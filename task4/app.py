from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import date, timedelta, datetime, time
import configparser
import os
from bson.objectid import ObjectId
from pymongo import MongoClient

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)

# Config loading
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_path)
print("Sections loaded from config:", config.sections())

# MongoDB setup
MONGO_URI = config.get('DB', 'MONGO_URI', fallback='mongodb://localhost:27017')
DB_NAME = config.get('DB', 'DB_NAME', fallback='libraryDB')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
authors_col = db.author
publishers_col = db.publisher
genres_col = db.genre
books_col = db.books
borrowers_col = db.borrower


# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/viewer.html')
def viewer():
    return render_template('viewer.html')


@app.route('/api/books')
def get_books():
    # Aggregate to join collections manually
    pipeline = [
        {
            "$lookup": {
                "from": "author",
                "localField": "authID",
                "foreignField": "authID",
                "as": "author"
            }
        },
        {"$unwind": {"path": "$author", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup": {
                "from": "publisher",
                "localField": "pubID",
                "foreignField": "pubID",
                "as": "publisher"
            }
        },
        {"$unwind": {"path": "$publisher", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup": {
                "from": "genre",
                "localField": "genreID",
                "foreignField": "genreID",
                "as": "genre"
            }
        },
        {"$unwind": {"path": "$genre", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup": {
                "from": "borrower",
                "localField": "BID",
                "foreignField": "BID",
                "as": "borrower"
            }
        },
        {
            "$unwind": {"path": "$borrower", "preserveNullAndEmptyArrays": True}
        },
        {
            "$project": {
                "_id": 0,
                "BID": 1,
                "title": 1,
                "authID": 1,
                "pubID": 1,
                "genreID": 1,
                "author": "$author.auth_name",
                "publisher": "$publisher.pub_name",
                "genre": "$genre.genre_name",
                "borrower_name": "$borrower.borrower_name",
                "borrower_date": "$borrower.borrower_date",
                "return_date": "$borrower.return_date",
                "available": 1
            }
        }
    ]

    books = list(books_col.aggregate(pipeline))

    # Convert dates to isoformat strings
    for b in books:
        if b.get("borrower_date"):
            b["borrower_date"] = b["borrower_date"].isoformat()
        if b.get("return_date"):
            b["return_date"] = b["return_date"].isoformat()

    return jsonify(books)


@app.route('/api/books/<book_id>/borrow', methods=['POST'])
def borrow_book(book_id):
    book = books_col.find_one({"BID": book_id})
    if not book or not book.get("available", True):
        return jsonify({'error': 'Book not available'}), 400

    borrower_name = request.json.get('borrower_name', 'Anonymous')
    borrow_date = datetime.combine(date.today(), time.min)  # 00:00:00 time
    return_date = borrow_date + timedelta(days=7)

    # Generate BorrowerID (simple unique id)
    borrower_id = f"BR{book_id[-3:]}"  # same as before

    new_borrow = {
        "BorrowerID": borrower_id,
        "BID": book_id,
        "borrower_name": borrower_name,
        "borrower_date": borrow_date,
        "return_date": return_date
    }

    # Insert borrow record
    borrowers_col.insert_one(new_borrow)
    # Update book availability
    books_col.update_one({"BID": book_id}, {"$set": {"available": False}})

    return jsonify({'message': f'Book {book_id} borrowed successfully'})


@app.route('/api/books/<book_id>/return', methods=['POST'])
def return_book(book_id):
    book = books_col.find_one({"BID": book_id})
    if not book or book.get("available", True):
        return jsonify({'error': 'Book is not borrowed'}), 400

    # Delete all borrower records for this book
    borrowers_col.delete_many({"BID": book_id})

    # Mark book as available
    books_col.update_one({"BID": book_id}, {"$set": {"available": True}})

    return jsonify({'message': f'Book {book_id} returned successfully'})


@app.route('/api/borrowers/clear', methods=['DELETE'])
def clear_all_borrow_records():
    try:
        # Set all books available
        books_col.update_many({}, {"$set": {"available": True}})
        # Delete all borrower records
        borrowers_col.delete_many({})
        return jsonify({'message': 'All borrow records cleared'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/books/<book_id>')
def get_book(book_id):
    pipeline = [
        {"$match": {"BID": book_id}},
        {
            "$lookup": {
                "from": "author",
                "localField": "authID",
                "foreignField": "authID",
                "as": "author"
            }
        },
        {"$unwind": {"path": "$author", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup": {
                "from": "publisher",
                "localField": "pubID",
                "foreignField": "pubID",
                "as": "publisher"
            }
        },
        {"$unwind": {"path": "$publisher", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup": {
                "from": "genre",
                "localField": "genreID",
                "foreignField": "genreID",
                "as": "genre"
            }
        },
        {"$unwind": {"path": "$genre", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup": {
                "from": "borrower",
                "localField": "BID",
                "foreignField": "BID",
                "as": "borrower"
            }
        },
        {"$unwind": {"path": "$borrower", "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
                "_id": 0,
                "BID": 1,
                "title": 1,
                "author": "$author.auth_name",
                "publisher": "$publisher.pub_name",
                "genre": "$genre.genre_name",
                "borrower_name": "$borrower.borrower_name",
                "borrower_date": "$borrower.borrower_date",
                "return_date": "$borrower.return_date",
                "available": 1
            }
        }
    ]

    book = list(books_col.aggregate(pipeline))
    if not book:
        return {"error": "Book not found"}, 404

    b = book[0]
    if b.get("borrower_date"):
        b["borrower_date"] = b["borrower_date"].isoformat()
    if b.get("return_date"):
        b["return_date"] = b["return_date"].isoformat()

    return b


@app.route('/api/authors/<auth_id>')
def get_author(auth_id):
    author = authors_col.find_one({"authID": auth_id}, {"_id": 0})
    if not author:
        return {"error": "Author not found"}, 404
    return author


@app.route('/api/publishers/<pub_id>')
def get_publisher(pub_id):
    publisher = publishers_col.find_one({"pubID": pub_id}, {"_id": 0})
    if not publisher:
        return {"error": "Publisher not found"}, 404
    return publisher


@app.route('/api/genres/<genre_id>')
def get_genre(genre_id):
    genre = genres_col.find_one({"genreID": genre_id}, {"_id": 0})
    if not genre:
        return {"error": "Genre not found"}, 404
    return genre


if __name__ == '__main__':
    app.run(debug=True)
