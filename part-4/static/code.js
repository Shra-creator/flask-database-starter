const API = "/api";

/* ================= AUTHORS ================= */

function loadAuthors() {
    fetch(`${API}/authors`)
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("authorList");
            const authorSelect = document.getElementById("book_author_id");

            list.innerHTML = "";
            authorSelect.innerHTML = "<option value=''>Select Author</option>";

            data.authors.forEach(a => {
                // Author cards
                list.innerHTML += `
                    <div class="card">
                        <h3>${a.name}</h3>
                        <p><strong>City:</strong> ${a.city || "-"}</p>
                        <p><strong>Bio:</strong> ${a.bio || "-"}</p>
                        <button onclick="editAuthor(${a.id})">Edit</button>
                        <button onclick="deleteAuthor(${a.id})">Delete</button>
                    </div>
                `;

                // Dropdown option
                authorSelect.innerHTML += `
                    <option value="${a.id}">${a.name}</option>
                `;
            });
        });
}

function addAuthor() {
    fetch(`${API}/authors`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: document.getElementById("auth_name").value,
            city: document.getElementById("auth_city").value,
            bio: document.getElementById("auth_bio").value
        })
    })
    .then(res => res.json())
    .then(() => {
        document.getElementById("auth_name").value = "";
        document.getElementById("auth_city").value = "";
        document.getElementById("auth_bio").value = "";

        showAuthors();   // 🔥 THIS WAS MISSING
    });
}


function deleteAuthor(id) {
    fetch(`${API}/authors/${id}`, { method: "DELETE" })
        .then(() => loadAuthors());
}

function editAuthor(id) {
    const name = prompt("Enter new name:");
    const city = prompt("Enter new city:");
    const bio = prompt("Enter new bio:");

    fetch(`${API}/authors/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, city, bio })
    }).then(() => loadAuthors());
}

/* ================= BOOKS ================= */

function loadBooks() {
    fetch(`${API}/books `)
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("bookList");
            list.innerHTML = "";

            data.books.forEach(b => {
                list.innerHTML += `
                    <div class="card">
                        <h3>${b.title}</h3>
                        <p><strong>Author:</strong> ${b.author.name}</p>
                        <p><strong>Year:</strong> ${b.year || "-"}</p>
                        <p><strong>ISBN:</strong> ${b.isbn || "-"}</p>
                        <button onclick="editBook(${b.id})">Edit</button>
                        <button onclick="deleteBook(${b.id})">Delete</button>
                    </div>
                `;
            });
        });
}

function addBook() {
    fetch(`${API}/books`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            title: document.getElementById("book_title").value,
            year: parseInt(document.getElementById("book_year").value),
            isbn: document.getElementById("book_isbn").value,
            author_id: parseInt(document.getElementById("book_author_id").value)
        })
    }).then(() => {
        document.getElementById("book_title").value = "";
        document.getElementById("book_year").value = "";
        document.getElementById("book_isbn").value = "";
        document.getElementById("book_author_id").value = "";
        loadBooks();
    });
}

function deleteBook(id) {
    fetch(`${API}/books/${id}`, { method: "DELETE" })
        .then(() => loadBooks());
}

function editBook(id) {
    const title = prompt("Enter new title:");
    const year = parseInt(prompt("Enter new year:"));
    const isbn = prompt("Enter new ISBN:");
    const author_id = parseInt(prompt("Enter new author ID:"));

    fetch(`${API}/books/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, year, isbn, author_id })
    }).then(() => loadBooks());
}

/* ================= INIT ================= */

loadAuthors();
loadBooks();
