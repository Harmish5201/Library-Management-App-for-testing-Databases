const { MongoClient } = require('mongodb');

const url = 'mongodb://admin:root1234@localhost:27017/?authSource=admin';
const client = new MongoClient(url);

async function init() {
  try {
    await client.connect();
    console.log('Connected to MongoDB');

    const db = client.db('libraryDB');

    // Drop collections if exist to avoid duplicates on re-run
    const collections = await db.collections();
    for (const coll of collections) {
      await coll.drop().catch(() => {}); // ignore errors if collection doesn't exist
    }

    // Insert authors
    const authors = [
      { authID: "A01", auth_name: "Shakespiere", auth_desc: "writer" },
      { authID: "A02", auth_name: "Harmish", auth_desc: "not writer" },
      { authID: "A03", auth_name: "Priyang", auth_desc: "definitely not writer" },
      { authID: "A04", auth_name: "Guido van Rossum", auth_desc: "Inventor of Python programming language" },
      { authID: "A05", auth_name: "Miguel Grinberg", auth_desc: "Known for Flask web development" },
      { authID: "A06", auth_name: "Agatha Christie", auth_desc: "Renowned mystery writer" },
      { authID: "A07", auth_name: "J.K. Rowling", auth_desc: "Author of the fantasy Harry Potter series" },
    ];
    await db.collection('author').insertMany(authors);

    // Insert genres
    const genres = [
      { genreID: "G11", genre_name: "Rmantic", genre_desc: null },
      { genreID: "G12", genre_name: "Thriller", genre_desc: "So suspensetic" },
      { genreID: "G01", genre_name: "Comedy", genre_desc: "HAHA" },
      { genreID: "G02", genre_name: "Drama", genre_desc: "Serious narratives with emotional themes" },
      { genreID: "G03", genre_name: "Technology", genre_desc: "Books related to modern technology" },
      { genreID: "G04", genre_name: "Education", genre_desc: "Informative and instructional content" },
      { genreID: "G05", genre_name: "Sci-Fi", genre_desc: "Science fiction and futuristic tales" },
      { genreID: "G06", genre_name: "Mystery", genre_desc: "Whodunits and suspense thrillers" },
      { genreID: "G07", genre_name: "Fantasy", genre_desc: "Magical and otherworldly adventures" },
    ];
    await db.collection('genre').insertMany(genres);

    // Insert publishers
    const publishers = [
      { pubID: "P01", pub_name: "Tanna & co.", pub_desc: null },
      { pubID: "P02", pub_name: "Bhimani publishers", pub_desc: "publisher" },
      { pubID: "P03", pub_name: "TechWorld", pub_desc: "Focus on technology books" },
      { pubID: "P04", pub_name: "EduBooks Ltd.", pub_desc: "Educational content publisher" },
      { pubID: "P05", pub_name: "WebDev Press", pub_desc: "Specializes in web frameworks" },
      { pubID: "P06", pub_name: "MysteryHouse", pub_desc: "Thriller and crime stories" },
      { pubID: "P07", pub_name: "FantasyWorks", pub_desc: "Fantasy and magical tales" },
    ];
    await db.collection('publisher').insertMany(publishers);

    // Insert books
    const books = [
      { BID: "B101", authID: "A02", pubID: "P02", genreID: "G02", title: "Game of Codes", available: true },
      { BID: "B102", authID: "A03", pubID: "P03", genreID: "G03", title: "Linux Basics", available: true },
      { BID: "B104", authID: "A05", pubID: "P05", genreID: "G04", title: "Flask in Action", available: true },
      { BID: "B105", authID: "A06", pubID: "P06", genreID: "G06", title: "Murder on the Orient Express", available: true },
      { BID: "B108", authID: "A02", pubID: "P02", genreID: "G02", title: "Thrones and Codes", available: true },
      { BID: "B109", authID: "A01", pubID: "P01", genreID: "G01", title: "Gokuldham Diaries", available: true },
      { BID: "B100", authID: "A01", pubID: "P01", genreID: "G01", title: "tmkoc", available: true },
      { BID: "B107", authID: "A03", pubID: "P03", genreID: "G03", title: "Advanced Kernel Hacking", available: true },
      { BID: "B106", authID: "A07", pubID: "P07", genreID: "G07", title: "The Sorcerer Quest", available: true },
      { BID: "B103", authID: "A04", pubID: "P04", genreID: "G04", title: "Python Programming", available: true },
    ];
    await db.collection('books').insertMany(books);

    // Create empty borrower collection
    await db.createCollection('borrower');

    console.log('Database initialized with collections and data');
  } catch (err) {
    console.error('Error initializing MongoDB:', err);
  } finally {
    await client.close();
  }
}

init();
