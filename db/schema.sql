PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS fines;
DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS book_authors; -- junction
DROP TABLE IF EXISTS book_genres; -- junction
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS authors;


-- no author or genre ID since this is queried via junction table
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn TEXT UNIQUE CHECK (LENGTH(isbn) IN (10, 13)),
    title TEXT NOT NULL,
    language TEXT NOT NULL,
    is_high_demand BOOLEAN NOT NULL DEFAULT 0,
    stock_count INTEGER NOT NULL DEFAULT 0, -- over-normalised if in its own table (direct property of book)
    page_count INTEGER CHECK (page_count BETWEEN 1 AND 5000),
    synopsis TEXT CHECK (LENGTH(synopsis) <= 1000), -- character limit imposed
    publisher TEXT -- not publisher ID since no extra data about the publisher being stored
);

CREATE TABLE genres (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    age_rating INTEGER NOT NULL DEFAULT 0 CHECK (age_rating BETWEEN 0 AND 18),
    parent_genre_id INTEGER, -- self-referential for categories like fiction/non-fiction (default is NULL)
    FOREIGN KEY (parent_genre_id) REFERENCES genres(genre_id)
);

CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email_address TEXT UNIQUE NOT NULL, -- regex validation can be done in application code
    membership_start_date DATE NOT NULL DEFAULT CURRENT_DATE,
    date_of_birth DATE NOT NULL
);

CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    loan_date DATE NOT NULL DEFAULT CURRENT_DATE,
    return_by DATE NOT NULL,
    returned_at DATE,    -- NULL means still on loan
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);


-- zero-or-one to one relationship as returning loans in time prevents being fined
CREATE TABLE fines (
    loan_id INTEGER PRIMARY KEY, -- no surrogate key because each loan has one associated fine
    amount REAL NOT NULL, -- If default given, fine record created the instant the loan is.
    date_paid DATE,    -- NULL means unpaid
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id)
);

CREATE TABLE book_authors (
    book_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

CREATE TABLE book_genres (
    book_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (book_id, genre_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);
