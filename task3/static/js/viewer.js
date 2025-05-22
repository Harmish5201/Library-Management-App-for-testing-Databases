// viewer.js

window.onload = function () {
    const params = getQueryParams();
    const file = params['file'];
    const id = params['id'];
    //const params = new URLSearchParams(window.location.search);
    //const id = params.get("id");

    const handlerMap = {
        book: displayBook,
        author: displayAuthor,
        publisher: displayPublisher,
        genre: displayGenre
    };

    file && id ? (handlerMap[file]?.(id) ?? show404(file)) : showInvalidParams();
};

function show404(file) {
    document.getElementById('content').innerHTML = `<p>Error: ${file} database does not exist</p>`;
}

function showInvalidParams() {
    document.getElementById('content').innerHTML = '<p>Invalid parameters.</p>';
}


/**
 * Get query parameters from the URL.
 */
function getQueryParams() {
    const params = {};
    window.location.search.substring(1).split("&").forEach(pair => {
        const [key, value] = pair.split("=");
        if (key) {
            params[decodeURIComponent(key)] = decodeURIComponent(value || '');
        }
    });
    return params;
}

/**
 * Display an entity's details by fetching from the Flask API.
 */
async function displayBook(id) {
    try {
        // Fetch book data filtered by id
        const response = await fetch(`/api/books/${encodeURIComponent(id)}`);
        if (!response.ok) throw new Error('Book not found');

        const book = await response.json();
        console.log(book);

        let htmlContent = `<h1>Book Details</h1><ul>`;
        for (const [key, value] of Object.entries(book)) {
            if (key.toLowerCase() === 'bid' || key.toLowerCase() === 'id') continue;
            htmlContent += `<li><strong style="text-transform: capitalize;">${key}:</strong> ${value}</li>`;
        }
        htmlContent += `</ul>`;

        if (book.borrower_name) {
            htmlContent += `<h2>Borrowing Details</h2>
                <ul>
                    <li><strong>Borrower:</strong> ${book.borrower_name}</li>
                    <li><strong>Borrow Date:</strong> ${book.borrower_date}</li>
                    <li><strong>Return Date:</strong> ${book.return_date}</li>
                </ul>
                <button onclick="returnBook('${book.BID || book.id}')">Return Book</button>`;
        } else {
            htmlContent += `<p>This book is currently available for borrowing.</p>
                <button onclick="borrowBook('${book.BID || book.id}')">Borrow Book</button>`;
        }

        //htmlContent += `<a href="/" class="back-link">&larr; Back to Catalog</a>`;
        document.getElementById('content').innerHTML = htmlContent;

        // Fetch Gemini description
        //const entityName = book.title || book.name || 'Unknown';
        //fetchGeminiDescription(entityName);
        const descriptionMarkdown = book.description || 'No description available.';
        const descriptionHTML = marked.parse(descriptionMarkdown);
        document.getElementById('description').innerHTML = `<h2>Description</h2>${descriptionHTML}`;

    } catch (error) {
        console.error('Error displaying book:', error);
        document.getElementById('content').innerHTML = `<p>${error}</p>`;
    }
}

async function displayAuthor(id) {
    try {
        // Fetch author data filtered by id
        const response = await fetch(`/api/authors/${encodeURIComponent(id)}`);
        if (!response.ok) throw new Error('Author not found');

        const author = await response.json();
        console.log(author);

        let htmlContent = `<h1>Author Details</h1><ul>`;
        for (const [key, value] of Object.entries(author)) {
            if (key.toLowerCase() === 'description' || key.toLowerCase() === 'id') continue;
            htmlContent += `<li style="list-style-type: none;"><strong style="text-transform: capitalize;">${key}:</strong> ${value}</li>`;
        }
        htmlContent += `</ul>`;

        document.getElementById('content').innerHTML = htmlContent;
        const descriptionMarkdown = author.description || 'No description available.';
        const descriptionHTML = marked.parse(descriptionMarkdown);
        document.getElementById('description').innerHTML = `<h2>Description</h2>${descriptionHTML}`;

    } catch (error) {
        console.error('Error displaying Author:', error);
        document.getElementById('content').innerHTML = `<p>${error}</p>`;
    }
}

async function displayPublisher(id) {
        try {
        // Fetch publisher data filtered by id
        const response = await fetch(`/api/publishers/${encodeURIComponent(id)}`);
        if (!response.ok) throw new Error('Publisher not found');

        const publisher = await response.json();
        console.log(publisher);

        let htmlContent = `<h1>Publisher Details</h1><ul>`;
        for (const [key, value] of Object.entries(publisher)) {
            if (key.toLowerCase() === 'description' || key.toLowerCase() === 'id') continue;
            htmlContent += `<li style="list-style-type: none;"><strong style="text-transform: capitalize;">${key}:</strong> ${value}</li>`;
        }
        htmlContent += `</ul>`;

        document.getElementById('content').innerHTML = htmlContent;
        const descriptionMarkdown = publisher.description || 'No description available.';
        const descriptionHTML = marked.parse(descriptionMarkdown);
        document.getElementById('description').innerHTML = `<h2>Description</h2>${descriptionHTML}`;

    } catch (error) {
        console.error('Error displaying publisher:', error);
        document.getElementById('content').innerHTML = `<p>${error}</p>`;
    }
}
async function displayGenre(id) {
        try {
        // Fetch publisher data filtered by id
        const response = await fetch(`/api/genres/${encodeURIComponent(id)}`);
        if (!response.ok) throw new Error('Genre not found');

        const genre = await response.json();
        console.log(genre);

        let htmlContent = `<h1>Genre Details</h1><ul>`;
        for (const [key, value] of Object.entries(genre)) {
            if (key.toLowerCase() === 'description' || key.toLowerCase() === 'id') continue;
            htmlContent += `<li style="list-style-type: none;"><strong style="text-transform: capitalize;">${key}:</strong> ${value}</li>`;
        }
        htmlContent += `</ul>`;

        document.getElementById('content').innerHTML = htmlContent;
        const descriptionMarkdown = genre.description || 'No description available.';
        const descriptionHTML = marked.parse(descriptionMarkdown);
        document.getElementById('description').innerHTML = `<h2>Description</h2>${descriptionHTML}`;

    } catch (error) {
        console.error('Error displaying genre:', error);
        document.getElementById('content').innerHTML = `<p>${error}</p>`;
    }
}























    function borrowBook(BID) {
    fetch(`/api/books/${BID}/borrow`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ borrower_name: 'Anonymous' })  // Replace with actual user input if needed
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || 'Book borrowed!');
        location.reload();
    })
    .catch(error => {
        console.error('Borrow error:', error);
        alert('Failed to borrow the book');
    });
}

function returnBook(BID) {
    fetch(`/api/books/${BID}/return`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || 'Book returned!');
        location.reload();
    })
    .catch(error => {
        console.error('Return error:', error);
        alert('Failed to return the book');
    });
}
