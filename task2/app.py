from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import configparser
import requests
import logging
import os


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


class Librarian(db.Model):
    __tablename__ = 'librarian'
    librarianID = db.Column(db.String(5), primary_key=True)
    librarian_name = db.Column(db.String(25), nullable=False)
    shift = db.Column(db.String(10))
    hire_date = db.Column(db.Date)

# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/viewer.html')
def viewer():
    return render_template('viewer.html')


@app.route('/api/books', methods=['GET'])
def get_books():
    try:
        books = Book.query.all()
        results = [{
            'BID': book.BID,
            'title': book.title,
            'available': book.available,
            'author': book.author.auth_name if book.author else 'N/A',
            'publisher': book.publisher.pub_name if book.publisher else 'N/A',
            'genre': book.genre.genre_name if book.genre else 'N/A'
        } for book in books]
        return jsonify(results)
    except Exception as e:
        logging.exception("Error fetching books")
        
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)
