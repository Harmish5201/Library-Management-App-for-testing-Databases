# 📚 Library Management Task

This is a web-based Library Management System built using **Flask**, **MongoDB**, and **Vanilla JS**. It allows users to view, borrow, return, and manage books within a library catalog, with metadata such as authors, publishers, and genres.

---

## 🚀 Features

* View a full catalog of books with metadata
* Borrow and return books with date tracking
* View borrow status and due dates
* Admin option to clear all borrow records
* Dynamic viewer for book, author, publisher, and genre details

---

## ⚙️ Tech Stack

* **Backend**: Flask (Python), PyMongo
* **Frontend**: HTML/CSS + Vanilla JS
* **Database**: MongoDB (local or cloud)
* **Others**: CORS, DOMPurify, Marked.js, Docker (optional for MongoDB)

---

## 🛠️ Installation & Setup

1. **Clone this repo**

   ```bash
   git clone https://github.com/Harmish5201/DBBD
   cd task4
   ```

2. **Start Neo4j using Docker Compose**

   Ensure Docker is installed and running. Then execute:

   ```bash
   docker-compose up -d
   ```

   This will spin up a Neo4j instance with the configuration specified in `docker-compose.yaml`.

3. **Install Python dependencies**

   ```bash
   pip install flask flask_cors pymongo configparser
   ```

4. **Insert initial data**

   Insert data into MongoDB using cmd
   ```bash
   cd "MongoDB init"
   node init_mongo.js
   ```

5. **Run the server**

   ```bash
   python app.py
   ```

   Access the app at: [http://localhost:5000](http://localhost:5000)

---

## 💡 Notable Design & Implementation Decisions

* **Borrow/Return Logic**
  Books can only be borrowed if available. A borrow record is created and the book is marked unavailable.

* **Document Modeling**

  * Collections: `books`, `author`, `publisher`, `genre`, `borrower`
  * Book metadata is linked via IDs (e.g. `authID`, `pubID`, etc.)

* **Dynamic UI**
  JavaScript fetches API data and dynamically updates the catalog. UI reflects borrow/return status in real time.

* **Borrower ID Generation**
  Borrower ID is created using the last three characters of the book’s ID, prefixed with `BR`.

* **Admin Reset**
  `/api/borrowers/clear` resets all borrowing activity and sets all books as available.

---

## 🧑‍💻 Authors

Created by Harmish Tanna & Priyang Bhimani.