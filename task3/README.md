# 📚 Library Management Task

This is a web-based Library Management System built using **Flask**, **PostgreSQL**, and **Vanilla JS**. It allows users to view, borrow, return, and manage books within a library catalog, with metadata such as authors, publishers, and genres.

---

## 🚀 Features

-  View a full catalog of books with metadata
-  Borrow and return books with date management
-  View borrow status and due dates
-  Admin option to clear all borrow records
-  Dynamic viewer for book, author, publisher, and genre details
-  Integrates with Gemini API (optional) for enhanced content/description (placeholders in code)

---

## ⚙️ Tech Stack

- **Backend**: Flask (Python), SQLAlchemy ORM
- **Frontend**: HTML/CSS + Vanilla JS
- **Database**: PostgreSQL
- **API Integration**: Gemini API (configurable)
- **Others**: CORS, DOMPurify, Marked.js, configparser

---

## 🛠️ Installation & Setup

1. **Clone this repo**

   ```bash
   git clone https://github.com/Harmish5201/DBBD
   cd task2
   ```

2. **Install Python packages**

   ```bash
   pip install flask flask_sqlalchemy flask_cors python-dateutil psycopg2-binary
   ```

3. **Create `config.ini` in root**

   ```ini
    [DB]
    DB_NAME=postgres
    DB_USER=admin
    DB_PASSWORD=root
    DB_HOST=127.0.0.1
    DB_PORT=5432

    [API]
    GEMINI_API_KEY=AIzaSyAbZYfZ2DndbXt76PINdRRnlPM-0SVb3o8
    GEMINI_API_URL=https://aistudio.google.com/app/apikey
   ```

4. **Create the database schema**

   Ensure PostgreSQL is running, and run:
   // or please refer to .sql files (for prof.) for manual installation

   ```bash
   flask shell
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

5. **Run the server**

   ```bash
   python app.py
   ```

   Access at `http://localhost:5000`


---

## 💡 Notable Design & Implementation Decisions

- **Borrow/Return Logic**: Each book can only be borrowed by one borrower at a time. The availability is tracked via the `available` boolean flag in the `Book` model.

- **Relational Modeling**:
  - Used `ForeignKey` and `relationship()` in SQLAlchemy to model relationships across `Book`, `Author`, `Publisher`, `Genre`, and `Borrower`.
  - Implemented `outerjoin` to show all books even if they aren't currently borrowed.

- **Dynamic UI**:
  - JavaScript dynamically updates available/borrowed books and controls the borrow/return actions.
  - Borrow and return operations optimistically update the UI before confirming with the backend.

- **BorrowerID Generation**:
  - Borrower IDs are auto-generated based on the book ID for uniqueness and traceability.

- **Data Reset Option**:
  - An admin tool (`/api/borrowers/clear`) is exposed to clear all borrow records, useful for demos or resets.

---

## 🧑‍💻 Author

Created by Harmish Tanna & Priyang Bhimani.