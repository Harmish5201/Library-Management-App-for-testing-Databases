from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import date
from flask import jsonify
import configparser
import requests
import logging
import os
from dateutil.relativedelta import relativedelta


app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# Config loading
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_path)
print("Sections loaded from config:", config.sections())


# Gemini API
GEMINI_API_KEY = config.get('API', 'GEMINI_API_KEY', fallback=None)
GEMINI_API_URL = config.get('API', 'GEMINI_API_URL', fallback=None)

# Database setup
DB_NAME = config.get('DB', 'DB_NAME')
DB_USER = config.get('DB', 'DB_USER')
DB_PASSWORD = config.get('DB', 'DB_PASSWORD')
DB_HOST = config.get('DB', 'DB_HOST')
DB_PORT = config.get('DB', 'DB_PORT')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Author(db.Model):
    __tablename__ = 'author'
    authID = db.Column(db.String(5), primary_key=True)
    auth_name = db.Column(db.String(25), nullable=False)
    auth_desc = db.Column(db.String(250))


class Publisher(db.Model):
    __tablename__ = 'publisher'
    pubID = db.Column(db.String(5), primary_key=True)
    pub_name = db.Column(db.String(25), nullable=False)
    pub_desc = db.Column(db.String(250))


class Genre(db.Model):
    __tablename__ = 'genre'
    genreID = db.Column(db.String(5), primary_key=True)
    genre_name = db.Column(db.String(15), nullable=False)
    genre_desc = db.Column(db.String(250))


class Book(db.Model):
    __tablename__ = 'books'
    BID = db.Column(db.String(5), primary_key=True)
    authID = db.Column(db.String(5), db.ForeignKey('author.authID'), nullable=False)
    pubID = db.Column(db.String(5), db.ForeignKey('publisher.pubID'), nullable=False)
    genreID = db.Column(db.String(5), db.ForeignKey('genre.genreID'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean)

    author = db.relationship('Author', backref='books')
    publisher = db.relationship('Publisher', backref='books')
    genre = db.relationship('Genre', backref='books')

class Borrower(db.Model):
    __tablename__ = 'borrower'
    BorrowerID = db.Column(db.String(5), primary_key=True)
    BID = db.Column(db.String(5), db.ForeignKey('books.BID'), nullable=False)
    borrower_name = db.Column(db.String(25), nullable=False)
    borrower_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)

    book = db.relationship('Book', backref='borrowers')




# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/viewer.html')
def viewer():
    return render_template('viewer.html')


@app.route('/api/books')
def get_books():
    books = (
        db.session.query(
            Book.BID,
            Book.title,
            Author.auth_name.label("author"),
            Publisher.pub_name.label("publisher"),
            Genre.genre_name.label("genre"),
            Borrower.borrower_name,
            Borrower.borrower_date,
            Borrower.return_date
        )
        .join(Author, Book.authID == Author.authID)
        .join(Publisher, Book.pubID == Publisher.pubID)
        .join(Genre, Book.genreID == Genre.genreID)
        .outerjoin(Borrower, Book.BID == Borrower.BID)  # Left join borrower
        .all()
    )

    # Convert to list of dicts
    books_list = []
    for b in books:
        books_list.append({
            "BID": b.BID,
            "title": b.title,
            "author": b.author,
            "publisher": b.publisher,
            "genre": b.genre,
            "borrower_name": b.borrower_name,
            "borrower_date": b.borrower_date.isoformat() if b.borrower_date else None,
            "return_date": b.return_date.isoformat() if b.return_date else None,
        })

    return jsonify(books_list)

@app.route('/api/books/<book_id>/borrow', methods=['POST'])
def borrow_book(book_id):
    book = Book.query.get(book_id)
    if not book or not book.available:
        return jsonify({'error': 'Book not available'}), 400

    borrower_name = request.json.get('borrower_name', 'Anonymous')  # You can extend this later
    borrow_date = date.today()
    return_date = borrow_date + relativedelta(months=2)  # or borrow_date + timedelta(days=7)

    # Generate BorrowerID (this is basic logic, feel free to improve)
    borrower_id = f"BR{book_id[-3:]}"  # e.g., B105 → BR105

    new_borrow = Borrower(
        BorrowerID=borrower_id,
        BID=book.BID,
        borrower_name=borrower_name,
        borrower_date=borrow_date,
        return_date=return_date
    )

    book.available = False
    db.session.add(new_borrow)
    db.session.commit()
    return jsonify({'message': f'Book {book_id} borrowed successfully'})


@app.route('/api/books/<book_id>/return', methods=['POST'])
def return_book(book_id):
    book = Book.query.get(book_id)
    if not book or book.available:
        return jsonify({'error': 'Book is not borrowed'}), 400

    # Find borrower record(s) for this book and delete them
    borrowers = Borrower.query.filter_by(BID=book_id).all()
    for borrower in borrowers:
        db.session.delete(borrower)

    # Mark book as available
    book.available = True

    db.session.commit()
    return jsonify({'message': f'Book {book_id} returned successfully'})

@app.route('/api/clear', methods=['DELETE'])
def clear_borrow_data():
    try:
        db.session.query(Borrower).delete()
        for book in Book.query.all():
            book.available = True
        db.session.commit()
        return jsonify({"message": "All borrow data cleared"}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error("Error clearing borrow data: %s", e)
        return jsonify({"error": "Failed to clear borrowing data"}), 500



if __name__ == '__main__':
    app.run(debug=True)
