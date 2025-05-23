from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import date, timedelta
import configparser
import logging
import os
from neo4j import GraphDatabase

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# Config loading
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_path)
print("Sections loaded from config:", config.sections())

# Load DB
NEO4J_URI = config.get('NEO4J', 'NEO4J_URI')
NEO4J_USER = config.get('NEO4J', 'NEO4J_USER')
NEO4J_PASSWORD = config.get('NEO4J', 'NEO4J_PASSWORD')

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/viewer.html')
def viewer():
    return render_template('viewer.html')

@app.route('/api/books')
def get_books():
    with driver.session() as session:
        result = session.run("""
            MATCH (b:Book)-[:WRITTEN_BY]->(a:Author),
                  (b)-[:PUBLISHED_BY]->(p:Publisher),
                  (b)-[:BELONGS_TO]->(g:Genre)
            OPTIONAL MATCH (b)<-[:BORROWED]-(br:Borrower)
            RETURN b.BID AS BID, b.title AS title,b.available AS available,
                   a.authID AS authID, a.auth_name AS author, a.auth_desc AS author_desc,
                   p.pubID AS pubID, p.pub_name AS publisher,
                   g.genreID AS genreID, g.genre_name AS genre,
                   br.borrower_name AS borrower_name, 
                   toString(coalesce(br.borrowed_date, br.borrower_date)) AS borrowed_date,    
                   toString(br.return_date) AS return_date
        """)
        books_list = []
        for record in result:
            books_list.append({
                "BID": record["BID"],
                "title": record["title"],
                "author": record["author"],
                "author_desc": record["author_desc"],
                "authID": record["authID"],
                "publisher": record["publisher"],
                "pubID": record["pubID"],
                "genre": record["genre"],
                "genreID": record["genreID"],
                "borrower_name": record["borrower_name"],
                "borrower_date": record["borrowed_date"],
                "return_date": record["return_date"],
                "available": record["available"],

            })
        return jsonify(books_list)

@app.route('/api/books/<book_id>/borrow', methods=['POST'])
def borrow_book(book_id):
    borrower_name = request.json.get('borrower_name', 'Anonymous')
    borrow_date = date.today().isoformat()
    return_date = (date.today() + timedelta(days=7)).isoformat()
    borrower_id = f"BR{book_id[-3:]}"  

    with driver.session() as session:
        result = session.run("""
            MATCH (b:Book {BID: $book_id})
            WHERE b.available = true
            SET b.available = false
            CREATE (br:Borrower {
                BorrowerID: $borrower_id,
                borrower_name: $borrower_name,
                borrowed_date: date($borrow_date),
                return_date: date($return_date)
            })
            CREATE (br)-[:BORROWED]->(b)
            RETURN b.BID AS BID
        """, book_id=book_id, borrower_id=borrower_id, borrower_name=borrower_name,
           borrow_date=borrow_date, return_date=return_date)
        record = result.single()
        if record:
            return jsonify({'message': f'Book {book_id} borrowed successfully'})
        else:
            return jsonify({'error': 'Book not available'}), 400

@app.route('/api/books/<book_id>/return', methods=['POST'])
def return_book(book_id):
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (b:Book {BID: $book_id})<-[:BORROWED]-(br:Borrower)
                SET b.available = true
                DETACH DELETE br
                RETURN b.BID AS BID
            """, book_id=book_id)
            record = result.single()

        if record:
            return jsonify({'message': f'Book {book_id} returned successfully'}), 200
        else:
            return jsonify({'error': 'Book not found or not borrowed'}), 200  # Still return 200 so JS doesn't break

    except Exception as e:
        # Log the error and return 200 with error message to avoid frontend failure
        print(f"[ERROR] Failed to return book {book_id}: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 200


@app.route('/api/borrowers/clear', methods=['DELETE'])
def clear_all_borrow_records():
    with driver.session() as session:
        session.run("""
            MATCH (br:Borrower)-[:BORROWED]->(b:Book)
            SET b.available = true
        """)
        session.run("""
            MATCH (br:Borrower)
            DETACH DELETE br
        """)
    return jsonify({'message': 'All borrow records cleared'}), 200


@app.route('/api/books/<book_id>')
def get_book(book_id):
    with driver.session() as session:
        result = session.run("""
            MATCH (b:Book {BID: $book_id})-[:WRITTEN_BY]->(a:Author),
                  (b)-[:PUBLISHED_BY]->(p:Publisher),
                  (b)-[:BELONGS_TO]->(g:Genre)
            OPTIONAL MATCH (b)<-[:BORROWED]-(br:Borrower)
            RETURN b.BID AS BID, b.title AS title,
                   a.auth_name AS author, a.auth_desc AS author_desc,
                   p.pub_name AS publisher, g.genre_name AS genre,
                   br.borrower_name AS borrower_name, br.borrowed_date AS borrowed_date, br.return_date AS return_date
        """, book_id=book_id)
        record = result.single()
        if record:
            return {
                "BID": record["BID"],
                "title": record["title"],
                "author": record["author"],
                "author_desc": record["author_desc"],
                "publisher": record["publisher"],
                "genre": record["genre"],
                "borrower_name": record["borrower_name"],
                "borrowed_date": str(record["borrowed_date"]) if record["borrowed_date"] else None,
                "return_date": str(record["return_date"]) if record["return_date"] else None,
            }
        else:
            return {"error": "Book not found"}, 404

@app.route('/api/authors/<auth_id>')
def get_author(auth_id):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Author {authID: $auth_id})
            RETURN a.authID AS id, a.auth_name AS name, a.auth_desc AS description
        """, auth_id=auth_id)
        record = result.single()
        if record:
            return {
                "id": record["id"],
                "name": record["name"],
                "description": record["description"]
            }
        else:
            return {"error": "Author not found"}, 404


@app.route('/api/publishers/<pub_id>')
def get_publisher(pub_id):
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Publisher {pubID: $pub_id})
            RETURN p.pubID AS id, p.pub_name AS name, p.pub_desc AS description
        """, pub_id=pub_id)
        record = result.single()
        if record:
            return {
                "id": record["id"],
                "name": record["name"],
                "description": record["description"]
            }
        else:
            return {"error": "Publisher not found"}, 404


@app.route('/api/genres/<genre_id>')
def get_genre(genre_id):
    with driver.session() as session:
        result = session.run("""
            MATCH (g:Genre {genreID: $genre_id})
            RETURN g.genreID AS id, g.genre_name AS name, g.genre_desc AS description
        """, genre_id=genre_id)
        record = result.single()
        if record:
            return {
                "id": record["id"],
                "name": record["name"],
                "description": record["description"]
            }
        else:
            return {"error": "Genre not found"}, 404

if __name__ == '__main__':
    app.run(debug=True)