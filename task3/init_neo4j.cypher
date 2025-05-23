LOAD CSV WITH HEADERS FROM 'file:///books.csv' AS row
MERGE (b:Book {BID: row.BID})
SET b.authID = row.authID,
    b.pubID = row.pubID,
    b.genreID = row.genreID,
    b.title = row.title,
    b.available = toBoolean(row.available);

LOAD CSV WITH HEADERS FROM 'file:///author.csv' AS row
MERGE (a:Author {authID: row.authID})
SET a.auth_name = row.auth_name,
    a.auth_desc = row.auth_desc;

LOAD CSV WITH HEADERS FROM 'file:///genre.csv' AS row
MERGE (g:Genre {genreID: row.genreID})
SET g.genre_name = row.genre_name,
    g.genre_desc = row.genre_desc;

LOAD CSV WITH HEADERS FROM 'file:///publisher.csv' AS row
MERGE (p:Publisher {pubID: row.pubID})
SET p.pub_name = row.pub_name,
    p.pub_desc = row.pub_desc;

LOAD CSV WITH HEADERS FROM 'file:///borrower.csv' AS row
MERGE (br:Borrower {BorrowerID: row.BorrowerID})
SET br.borrower_name = row.borrower_name,
    br.BID=row.BID,
    br.borrowed_date = date(row.borrower_date),  // Rename borrower_date to borrowed_date
    br.return_date = date(row.return_date);

LOAD CSV WITH HEADERS FROM 'file:///books.csv' AS row
MATCH (a:Author {authID: row.authID}), (b:Book {BID: row.BID})
MERGE (b)-[:WRITTEN_BY]->(a);

LOAD CSV WITH HEADERS FROM 'file:///books.csv' AS row
MATCH (g:Genre {genreID: row.genreID}), (b:Book {BID: row.BID})
MERGE (b)-[:BELONGS_TO]->(g);

LOAD CSV WITH HEADERS FROM 'file:///books.csv' AS row
MATCH (p:Publisher {pubID: row.pubID}), (b:Book {BID: row.BID})
MERGE (b)-[:PUBLISHED_BY]->(p);

LOAD CSV WITH HEADERS FROM 'file:///borrower.csv' AS row
MATCH (br:Borrower {BorrowerID: row.BorrowerID}), (b:Book {BID: row.BID})
MERGE (br)-[:BORROWED]->(b);

MATCH (br:Borrower) RETURN br LIMIT 25

MATCH (n)-[r]->(m) RETURN n, r, m

