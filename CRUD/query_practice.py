import sqlite3
from datetime import date


def get_high_demand_books(conn: sqlite3.Connection) -> list[str]:
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM books WHERE is_high_demand = 1")
    # list comprehension needed o/w a list of 1 element tuples is returned
    return [title for (title,) in cursor.fetchall()]


def get_members_born_before_1990(conn: sqlite3.Connection) -> list[str]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM members WHERE date_of_birth < '1990-01-01'"
        )
    return [name for (name,) in cursor.fetchall()]


def get_books_with_more_than_n_stock(
        conn: sqlite3.Connection, n: int
        ) -> list[str]:
    """
    Challenge:
    List all books with more than 3 in stock, ordered by stock count descending
    """
    cursor = conn.cursor()
    cursor.execute(
        "SELECT title FROM books WHERE stock_count > ? "
        "ORDER BY stock_count DESC", (n,)
        )
    return [title for (title,) in cursor.fetchall()]


def get_different_languages_count(
        conn: sqlite3.Connection
        ) -> list[tuple[str, int]]:
    cursor = conn.cursor()
    cursor.execute("SELECT language, COUNT(*) FROM books "
                   "GROUP BY language")
    return cursor.fetchall()


def get_active_loans(conn: sqlite3.Connection) -> list[tuple[str, str]]:
    """
    Challenge:
    List all active loans (not yet returned) with the member's
    name and book title
    """
    cursor = conn.cursor()
    cursor.execute("SELECT members.name, books.title FROM members JOIN "
                   "loans on members.member_id = loans.member_id JOIN books "
                   "on loans.book_id = books.book_id WHERE loans.returned_at "
                   "IS NULL")
    return cursor.fetchall()


def get_authors_for_books(conn: sqlite3.Connection) -> dict[str, list[str]]:
    # List each book with its authors' names
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT books.title, authors.name
                   FROM books
                   JOIN book_authors ON books.book_id = book_authors.book_id
                   JOIN authors ON book_authors.author_id = authors.author_id
                   """)
    # result = {}
    # for title, author in cursor.fetchall():
    #     if title not in result:
    #         result[title] = [author]
    #         continue
    #     result[title].append(author)
    results = {}
    for title, author in cursor.fetchall():
        results.setdefault(title, []).append(author)  # setdefault is simpler
    return results


def get_members_who_never_loaned(conn: sqlite3.Connection) -> list[str]:
    cursor = conn.cursor()
    # Below is an example of a subquery
    # cursor.execute("""
    #                SELECT name FROM members
    #                WHERE member_id NOT IN (SELECT member_id FROM loans)
    #                """)

    # Below is the left join approach (more standard)
    cursor.execute("""
                   SELECT members.name FROM members
                   LEFT JOIN loans ON members.member_id = loans.member_id
                   WHERE loans.member_id IS NULL
                   """)
    return [name for (name,) in cursor.fetchall()]


def get_overdue_loans(conn: sqlite3.Connection) -> list[tuple[str, str]]:
    """
    Find all overdue loans (return_by has passed, returned_at is NULL)
    with member name and book title
    """
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT members.name, books.title FROM members
                   JOIN loans on members.member_id = loans.member_id
                   JOIN books on loans.book_id = books.book_id
                   WHERE (returned_at IS NULL AND ? > return_by)
                   """, (date.today().isoformat(),))
    return cursor.fetchall()


def get_all_loan_details(
        conn: sqlite3.Connection
        ) -> list[tuple[str, str, float | None]]:
    """
    List all loans with member name, book title, and fine amount (if any)
    """
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT members.name, books.title, fines.amount
                   FROM members JOIN loans
                   ON members.member_id = loans.member_id
                   JOIN books ON loans.book_id = books.book_id
                   LEFT JOIN fines ON loans.loan_id = fines.loan_id
                   """)
    # The first attempt uses an inner join between loans and fines, which only
    # returns rows when a match exists in all tables. Therefore, I only get
    # the loans with a fine, rather than all loans regardless of fine.
    # Therefore, I am now using a LEFT JOIN between from loans to fines.
    return cursor.fetchall()


def get_all_unpaid_fines(
        conn: sqlite3.Connection
        ) -> list[tuple[str, str, float]]:
    """
    List members who have an unpaid fine, with the fine amount and book title
    """
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT members.name, books.title, fines.amount
                   FROM members JOIN loans
                   ON members.member_id = loans.member_id
                   JOIN books ON loans.book_id = books.book_id
                   JOIN fines ON loans.loan_id = fines.loan_id
                   WHERE fines.date_paid IS NULL
                   """)
    # Same SQL as get_all_loan_details but with an inner join at
    # the end rather than a left join.
    return cursor.fetchall()


def get_genres_of_books(
        conn: sqlite3.Connection
        ) -> dict[str, list[str | None]]:
    """
    LEFT JOINs are used such that books without a genre are still included
    The final SQL line is so I can get the parent genre of each subgenre.
    """
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT books.title, genres.name, parent.name
                   FROM books
                   LEFT JOIN book_genres ON books.book_id = book_genres.book_id
                   LEFT JOIN genres ON book_genres.genre_id = genres.genre_id
                   LEFT JOIN genres AS parent
                   ON genres.parent_genre_id = parent.genre_id
                   """)
    results = {}
    for title, genre, parent in cursor.fetchall():
        if not results.get(title) and parent:
            results[title] = [parent]
        results.setdefault(title, []).append(genre)  # setdefault is simpler
    return results


def get_loan_counts(conn: sqlite3.Connection) -> list[tuple[str, int]]:
    """
    Count how many loans each member has taken out, ordered by most loans first
    """
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT members.name, COUNT(*)
                   FROM members
                   JOIN loans ON members.member_id = loans.member_id
                   GROUP BY members.member_id
                   ORDER BY COUNT(*) DESC
                   """)
    # The join combines the members and loans table,
    # then group by collapses all entries with the same member ID
    # into one, i.e. records associated with the same member but different
    # loans are grouped - each group has a count and we return the query
    # from most to least loans
    return cursor.fetchall()


def get_average_overdue_loan_fine(conn: sqlite3.Connection) -> float:
    """
    Find the average fine amount for overdue loans
    """
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT AVG(amount) FROM fines
                   WHERE date_paid is NULL
                   """)
    average_fine = cursor.fetchone()[0]
    return 0 if average_fine is None else round(average_fine, 2)


def get_most_popular_subgenre(conn: sqlite3.Connection) -> str:
    """
    Which genre has the most books assigned to it?
    I'm excluding the fiction/non-fiction parent genres (trivial)
    """
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT genres.name FROM genres
                   JOIN book_genres ON genres.genre_id = book_genres.genre_id
                   WHERE genres.parent_genre_id IS NOT NULL
                   GROUP BY genres.genre_id
                   ORDER BY COUNT(*) DESC
                   LIMIT 1
                   """)
    # LIMIT 1 ensures the max cout genre is returned. If ASC ordering
    # was used, then LIMIT 1 would give the minimum count genre.
    return cursor.fetchone()[0]


def get_books_never_loaned(conn: sqlite3.Connection) -> list[str]:
    """
    Requires a subquery to be made
    """
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT title FROM books
                   WHERE book_id NOT IN (SELECT book_id FROM loans)
                   """)
    return [title for (title,) in cursor.fetchall()]


def get_members_with_fines_exceeding(
        conn: sqlite3.Connection, n: float
        ) -> list[str]:
    """
    Challenge:
    List members whose total unpaid fines exceed £5
    """
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT members.name FROM members
                   JOIN loans ON members.member_id = loans.member_id
                   JOIN fines ON loans.loan_id = fines.loan_id
                   WHERE fines.date_paid IS NULL
                   GROUP BY members.member_id
                   HAVING SUM(fines.amount) > ?
                   """, (n,))
    return [name for (name,) in cursor.fetchall()]


def get_most_borrowed_book(conn: sqlite3.Connection) -> str:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT title FROM books
                   JOIN loans ON books.book_id = loans.book_id
                   GROUP BY books.book_id
                   ORDER BY COUNT(*) DESC
                   LIMIT 1
                   """)
    return cursor.fetchone()[0]


def get_fiction_subgenres(conn: sqlite3.Connection) -> list[str]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT name FROM genres
                   WHERE genres.parent_genre_id =
                   (SELECT genre_id FROM genres where name LIKE 'fiction')
                   """)
    return [genre for (genre,) in cursor.fetchall()]
