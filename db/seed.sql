-- GENRES (parent genres first due to self-referential FK)
INSERT INTO genres (name, age_rating, parent_genre_id) VALUES ('Fiction', 0, NULL);      -- pk = 1
INSERT INTO genres (name, age_rating, parent_genre_id) VALUES ('Non-Fiction', 0, NULL);  -- pk = 2
INSERT INTO genres (name, age_rating, parent_genre_id) VALUES ('Mystery', 0, 1);         -- pk = 3
INSERT INTO genres (name, age_rating, parent_genre_id) VALUES ('Sci-Fi', 12, 1);         -- pk = 4
INSERT INTO genres (name, age_rating, parent_genre_id) VALUES ('Biography', 0, 2);       -- pk = 5
INSERT INTO genres (name, age_rating, parent_genre_id) VALUES ('Horror', 15, 1);         -- pk = 6
INSERT INTO genres (name, age_rating, parent_genre_id) VALUES ('History', 0, 2);         -- pk = 7
INSERT INTO genres (name, age_rating, parent_genre_id) VALUES ('Thriller', 15, 1);       -- pk = 8

-- AUTHORS
INSERT INTO authors (name) VALUES ('George Orwell');       -- pk = 1
INSERT INTO authors (name) VALUES ('Agatha Christie');     -- pk = 2
INSERT INTO authors (name) VALUES ('Stephen King');        -- pk = 3
INSERT INTO authors (name) VALUES ('Frank Herbert');       -- pk = 4
INSERT INTO authors (name) VALUES ('Arthur C. Clarke');    -- pk = 5
INSERT INTO authors (name) VALUES ('Aldous Huxley');       -- pk = 6
INSERT INTO authors (name) VALUES ('Yuval Noah Harari');   -- pk = 7
INSERT INTO authors (name) VALUES ('Walter Isaacson');     -- pk = 8

-- BOOKS
INSERT INTO books (title, language, is_high_demand, stock_count, page_count, publisher) VALUES ('1984', 'English', 1, 3, 328, 'Secker & Warburg');
INSERT INTO books (title, language, is_high_demand, stock_count, page_count, publisher) VALUES ('Murder on the Orient Express', 'English', 0, 5, 256, 'Collins Crime Club');
INSERT INTO books (title, language, is_high_demand, stock_count, page_count, publisher) VALUES ('The Shining', 'English', 0, 4, 447, 'Doubleday');
INSERT INTO books (title, language, is_high_demand, stock_count, page_count, publisher) VALUES ('Dune', 'English', 1, 2, 412, 'Chilton Books');
INSERT INTO books (title, language, is_high_demand, stock_count, page_count, publisher) VALUES ('2001: A Space Odyssey', 'English', 0, 6, 297, 'New American Library');
INSERT INTO books (title, language, is_high_demand, stock_count, page_count, publisher) VALUES ('Brave New World', 'English', 1, 2, 311, 'Chatto & Windus');
INSERT INTO books (title, language, is_high_demand, stock_count, page_count, publisher) VALUES ('Sapiens', 'English', 1, 1, 443, 'Harvill Secker');
INSERT INTO books (title, language, is_high_demand, stock_count, page_count, publisher) VALUES ('Steve Jobs', 'English', 0, 3, 656, 'Simon & Schuster');
INSERT INTO books (title, language, is_high_demand, stock_count, page_count, publisher) VALUES ('Animal Farm', 'English', 0, 7, 112, 'Secker & Warburg');
INSERT INTO books (title, language, is_high_demand, stock_count, page_count, publisher) VALUES ('It', 'English', 0, 2, 1138, 'Viking');

-- BOOK AUTHORS (junction)
INSERT INTO book_authors (book_id, author_id) VALUES (1, 1);   -- 1984 → Orwell
INSERT INTO book_authors (book_id, author_id) VALUES (2, 2);   -- Orient Express → Christie
INSERT INTO book_authors (book_id, author_id) VALUES (3, 3);   -- The Shining → King
INSERT INTO book_authors (book_id, author_id) VALUES (4, 4);   -- Dune → Herbert
INSERT INTO book_authors (book_id, author_id) VALUES (5, 5);   -- 2001 → Clarke
INSERT INTO book_authors (book_id, author_id) VALUES (6, 6);   -- Brave New World → Huxley
INSERT INTO book_authors (book_id, author_id) VALUES (7, 7);   -- Sapiens → Harari
INSERT INTO book_authors (book_id, author_id) VALUES (8, 8);   -- Steve Jobs → Isaacson
INSERT INTO book_authors (book_id, author_id) VALUES (9, 1);   -- Animal Farm → Orwell (same author as 1984)
INSERT INTO book_authors (book_id, author_id) VALUES (10, 3);  -- It → King (same author as The Shining)

-- BOOK GENRES (junction) -- some books span multiple genres
INSERT INTO book_genres (book_id, genre_id) VALUES (1, 4);   -- 1984 → Sci-Fi
INSERT INTO book_genres (book_id, genre_id) VALUES (1, 8);   -- 1984 → Thriller
INSERT INTO book_genres (book_id, genre_id) VALUES (2, 3);   -- Orient Express → Mystery
INSERT INTO book_genres (book_id, genre_id) VALUES (2, 8);   -- Orient Express → Thriller
INSERT INTO book_genres (book_id, genre_id) VALUES (3, 6);   -- The Shining → Horror
INSERT INTO book_genres (book_id, genre_id) VALUES (4, 4);   -- Dune → Sci-Fi
INSERT INTO book_genres (book_id, genre_id) VALUES (5, 4);   -- 2001 → Sci-Fi
INSERT INTO book_genres (book_id, genre_id) VALUES (6, 4);   -- Brave New World → Sci-Fi
INSERT INTO book_genres (book_id, genre_id) VALUES (7, 7);   -- Sapiens → History
INSERT INTO book_genres (book_id, genre_id) VALUES (8, 5);   -- Steve Jobs → Biography
INSERT INTO book_genres (book_id, genre_id) VALUES (9, 1);   -- Animal Farm → Fiction
INSERT INTO book_genres (book_id, genre_id) VALUES (10, 6);  -- It → Horror

-- MEMBERS
INSERT INTO members (name, email_address, date_of_birth) VALUES ('Lewis Dean', 'lewis@outlook.com', '2003-05-22');
INSERT INTO members (name, email_address, date_of_birth) VALUES ('John Smith', 'john@gmail.com', '1985-11-20');
INSERT INTO members (name, email_address, date_of_birth) VALUES ('Sarah Connor', 'sarah@gmail.com', '1992-03-15');
INSERT INTO members (name, email_address, date_of_birth) VALUES ('Mike Taylor', 'mike@hotmail.com', '1978-07-04');
INSERT INTO members (name, email_address, date_of_birth) VALUES ('Emma Wilson', 'emma@outlook.com', '2000-12-01');
INSERT INTO members (name, email_address, date_of_birth) VALUES ('Bob Cratchit', 'bobby@icloud.com', '1880-12-01');

-- LOANS (mix of active, returned, and overdue)
INSERT INTO loans (book_id, member_id, loan_date, return_by) VALUES (1, 1, '2026-03-01', '2026-03-15');                            -- overdue, active
INSERT INTO loans (book_id, member_id, loan_date, return_by, returned_at) VALUES (2, 2, '2026-02-01', '2026-02-15', '2026-02-10'); -- returned on time
INSERT INTO loans (book_id, member_id, loan_date, return_by) VALUES (4, 1, '2026-03-10', '2026-03-24');                            -- active, due today
INSERT INTO loans (book_id, member_id, loan_date, return_by) VALUES (7, 3, '2026-02-20', '2026-03-06');                            -- overdue, active
INSERT INTO loans (book_id, member_id, loan_date, return_by, returned_at) VALUES (3, 4, '2026-01-10', '2026-01-24', '2026-01-30'); -- returned late
INSERT INTO loans (book_id, member_id, loan_date, return_by, returned_at) VALUES (6, 5, '2026-03-01', '2026-03-15', '2026-03-10'); -- returned on time
INSERT INTO loans (book_id, member_id, loan_date, return_by) VALUES (10, 2, '2026-03-15', '2026-03-29');                           -- active
INSERT INTO loans (book_id, member_id, loan_date, return_by, returned_at) VALUES (9, 3, '2026-01-01', '2026-01-15', '2026-01-14'); -- returned on time

-- FINES (only for overdue loans)
INSERT INTO fines (loan_id, amount) VALUES (1, 4.50);   -- Lewis, 1984 overdue
INSERT INTO fines (loan_id, amount) VALUES (4, 2.00);   -- Sarah, Sapiens overdue
INSERT INTO fines (loan_id, amount) VALUES (5, 3.00);   -- Mike, The Shining returned late (unpaid)
