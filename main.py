"""
11. List members who have an unpaid fine, with the fine amount and book title
"""
import sqlite3
import os
from datetime import date


def establish_db_connection(db_filename: str) -> sqlite3.Connection:
    db_exists = os.path.exists(db_filename)

    conn = sqlite3.connect(db_filename)  # will auto-create if does not exist
    conn.execute("PRAGMA foreign_keys = ON")  # PRAGMA does not persist in .db!
    # creates DB file if it did not exist prior to sqlite3.connect()
    if not db_exists:
        with open("schema.sql") as f:
            conn.executescript(f.read())
        with open("seed.sql") as f:
            conn.executescript(f.read())

    return conn


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
    # Thefirst attempt uses an inner join between loans and fines, which only
    # returns rows when a match exists in all tables. Therefore, I only get
    # the loans with a fine, rather than all loans regardless of fine.
    # Therefore, I am now using a LEFT JOIN between from loans to fines.
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


def main() -> None:
    conn = establish_db_connection("library.db")
    try:
        # print(get_high_demand_books(conn))
        # print(get_members_born_before_1990(conn))
        # print(get_books_with_more_than_n_stock(conn, 3))
        # print(get_different_languages_count(conn))
        # print(get_active_loans(conn))
        # print(get_members_who_never_loaned(conn))
        # print(get_authors_for_books(conn))
        # print(get_overdue_loans(conn))
        # print(get_all_loan_details(conn))
        print(get_genres_of_books(conn))
    except Exception as e:
        print(e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
