from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import configparser
import requests
import logging

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# Config loading
config = configparser.ConfigParser()

config.read(r'C:\Users\prite\library_management_task\config.ini')
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

# --- Models (exact column names preserved) ---

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
        # This is the key line to add:
        return jsonify({'error': str(e)}), 500


@app.route('/api/description', methods=['GET'])
def get_description():
    entity_name = request.args.get('name')
    if not entity_name:
        return jsonify({'error': 'Missing entity name'}), 400

    if not GEMINI_API_KEY or not GEMINI_API_URL:
        return jsonify({'error': 'Gemini API configuration missing'}), 500

    prompt = (
        f"Provide a detailed description of '{entity_name}'. "
        "If it is a book include information about the setting, characters, themes, key concepts, and its influence. "
        "Do not include any concluding remarks or questions. "
        "Do not mention any Note at the end about not including concluding remarks or questions."
    )

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code != 200:
            logging.error("Gemini API error: %s", response.text)
            return jsonify({'error': 'Failed to get description from Gemini'}), 500

        data = response.json()
        description = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        return jsonify({'description': description})
    except Exception as e:
        logging.exception("Error connecting to Gemini API")
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
