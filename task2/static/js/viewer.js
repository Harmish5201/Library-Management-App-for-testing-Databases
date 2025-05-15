// viewer.js

window.onload = function () {
    const params = getQueryParams();
    const file = params['file'];
    const id = params['id'];

    if (file && id) {
        displayEntity(file, id);
    } else {
        document.getElementById('content').innerHTML = '<p>Invalid parameters.</p>';
    }
};

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
 * Fetch description from Gemini API for an entity.
 */
async function fetchGeminiDescription(entityName) {
    try {
        const response = await fetch(`/api/description?name=${encodeURIComponent(entityName)}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.status === 400) {
            throw new Error('Invalid request. Entity name is missing.');
        } else if (response.status === 500) {
            throw new Error('Server error while fetching description.');
        } else if (!response.ok) {
            throw new Error('Unexpected error occurred.');
        }

        const data = await response.json();
        const descriptionMarkdown = data.description || 'No description available.';
        const descriptionHTML = marked.parse(descriptionMarkdown);
        document.getElementById('description').innerHTML = `<h2>Description</h2>${descriptionHTML}`;
    } catch (error) {
        console.error('Error fetching description from Gemini API:', error);
        document.getElementById('description').innerHTML = `<p>${error.message}</p>`;
    }
}

/**
 * Display an entity's details by fetching from the Flask API.
 */
async function displayEntity(file, id) {
    try {
        const fileToEndpointMap = {
            'books.xml': '/api/books',
            'authors.xml': '/api/authors',
            'publishers.xml': '/api/publishers',
            'genres.xml': '/api/genres'
        };

        const endpoint = fileToEndpointMap[file];
        if (!endpoint) {
            document.getElementById('content').innerHTML = '<p>Invalid file type.</p>';
            return;
        }

        const response = await fetch(endpoint);
        if (!response.ok) throw new Error('Failed to fetch data');
        const entities = await response.json();

        const entity = entities.find(item => item.BID === id || item.id === id);
        if (!entity) {
            document.getElementById('content').innerHTML = '<p>Entity not found.</p>';
            return;
        }

        const entityName = entity.title || entity.name || 'Unknown';

        let htmlContent = `<h1>${file.replace('.xml', '')} Details</h1><ul>`;
        for (const [key, value] of Object.entries(entity)) {
            if (key === 'BID' || key === 'id') continue;
            htmlContent += `<li><strong>${key}:</strong> ${value}</li>`;
        }
        htmlContent += '</ul>';

        // Borrowing Info for books
        if (file === 'books.xml') {
            const borrowingData = JSON.parse(localStorage.getItem('borrowingData')) || {};
            const borrowInfo = borrowingData[id];
            if (borrowInfo) {
                htmlContent += `<h2>Borrowing Details</h2>
                <ul>
                    <li><strong>Borrower:</strong> ${borrowInfo.borrowerName}</li>
                    <li><strong>Borrow Date:</strong> ${borrowInfo.borrowDate}</li>
                    <li><strong>Return Date:</strong> ${borrowInfo.returnDate}</li>
                </ul>`;
            } else {
                htmlContent += `<p>This book is currently available for borrowing.</p>`;
            }
        }

        htmlContent += `<a href="/" class="back-link">&larr; Back to Catalog</a>`;
        document.getElementById('content').innerHTML = htmlContent;

        // Fetch Gemini description
        if (entityName) {
            fetchGeminiDescription(entityName);
        }

    } catch (error) {
        console.error('Error displaying entity:', error);
        document.getElementById('content').innerHTML = `<p>Error loading entity details.</p>`;
    }
}
