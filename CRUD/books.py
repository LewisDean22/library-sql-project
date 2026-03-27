"""
CUD operations needed

Should there be a wrapper function called add_book
which calls add_book_record and add_author_record
since adding a book potentially requires a new author to be immediately
added - should be no book in the DB without an author or book_genres entry.

Also for delete_book, there should be a check to see if that author still
has any remaning books (maybe check for genre too), and if the answer is no,
they can be removed from the authors table.
"""
import sqlite3


def add_book_record(conn: sqlite3.Connection,
                    title: str,
                    language: str,
                    is_high_demand: bool,
                    isbn: str | None = None,
                    stock_count: int | None = None,
                    page_count: int | None = None,
                    synopsis: str | None = None,
                    publisher: str | None = None
                    ) -> None:
    """
    bool is an int subclass in Python so True/False
    will cast to 1/0 due to integer type affinity
    of the is_high_demand field.
    """
    fields = {
        "title": title,
        "language": language,
        "is_high_demand": is_high_demand
    }
    if isbn is not None:
        fields["isbn"] = isbn
    if stock_count is not None:
        fields["stock_count"] = stock_count
    if page_count is not None:
        fields["page_count"] = page_count
    if synopsis is not None:
        fields["synopsis"] = synopsis
    if publisher is not None:
        fields["publisher"] = publisher

    columns = ", ".join(fields.keys())
    placeholders = ", ".join(["?"] * len(fields))

    try:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO books ({columns}) VALUES ({placeholders})",
            tuple(fields.values())
            )
        conn.commit()
    except sqlite3.IntegrityError as e:
        # Needed if 5000 page limit exceeded, e.g.
        conn.rollback()
        raise ValueError(f"Invalid book data: {e}") from e
    except Exception as e:
        print(f"Error adding book: {e}")
        conn.rollback()  # redundant for one INSERT but good practice
