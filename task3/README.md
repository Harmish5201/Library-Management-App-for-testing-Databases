# 📚 Library Management Task

This is a web-based Library Management System built using **Flask**, **Neo4j**, and **Vanilla JS**. It allows users to view, borrow, return, and manage books within a library catalog, with metadata such as authors, publishers, and genres.

---

## 🚀 Features

- View a full catalog of books with metadata
- Borrow and return books with date tracking
- View borrow status and due dates
- Admin option to clear all borrow records
- Dynamic viewer for book, author, publisher, and genre details
- Integrates with Gemini API (optional) for enhanced content/description (placeholders in code)

---

## ⚙️ Tech Stack

- **Backend**: Flask (Python), Neo4j Driver
- **Frontend**: HTML/CSS + Vanilla JS
- **Database**: Neo4j (via Docker)
- **API Integration**: Gemini API (configurable)
- **Others**: CORS, DOMPurify, Marked.js, Docker Compose

---

## 🛠️ Installation & Setup

1. **Clone this repo**

   ```bash
   git clone https://github.com/Harmish5201/DBBD
   cd task3
````

2. **Start Neo4j using Docker Compose**

   Ensure Docker is installed and running. Then execute:

   ```bash
   docker-compose up -d
   ```

   This will spin up a Neo4j instance with the configuration specified in `docker-compose.yaml`.

3. **Install Python dependencies**

   ```bash
   pip install flask flask_cors neo4j configparser
   ```

4. **Initialize Neo4j data**

   Open the Neo4j browser at [http://localhost:7474](http://localhost:7474), log in with the default credentials (`neo4j` / `password` unless changed), and run the Cypher queries from `init_neo4j.cypher` file to populate the database schema and initial data.

5. **Run the server**

   ```bash
   python app.py
   ```

   Access the app at: [http://localhost:5000](http://localhost:5000)

---

## 💡 Notable Design & Implementation Decisions

* **Borrow/Return Logic**: Books can only be borrowed if available. When borrowed, a `Borrower` node is created and connected to the book via a `BORROWED` relationship.

* **Graph Modeling**:

  * Neo4j nodes represent `Book`, `Author`, `Publisher`, `Genre`, and `Borrower`.
  * Relationships define real-world connections such as `WRITTEN_BY`, `PUBLISHED_BY`, `BELONGS_TO`, and `BORROWED`.

* **Dynamic UI**:

  * JavaScript fetches data via API and dynamically updates the catalog and borrow/return status.
  * Optimistic UI updates ensure a smooth user experience.

* **Borrower ID Generation**:

  * `BorrowerID` is created uniquely using the last three characters of the Book ID for traceability.

* **Data Reset Option**:

  * Admin can clear all borrowing records via `/api/borrowers/clear`, which restores book availability and removes borrower nodes.

---

## 🧑‍💻 Author

Created by Harmish Tanna & Priyang Bhimani.