"""
CRUD TODO
- Omit genre CRUD for now
- Author CRUD needed if book CRUD in use
- Loans/fines CRUD will require interesting SQL
"""
import sqlite3
import os
from CRUD.members import add_member, update_member
from CRUD.books import add_book_record
from datetime import date
# from CRUD.query_practice import *


def establish_db_connection(db_filename: str,
                            rebuild: bool = False
                            ) -> sqlite3.Connection:
    db_exists = os.path.exists(db_filename)

    conn = sqlite3.connect(db_filename)  # will auto-create if does not exist
    conn.execute("PRAGMA foreign_keys = ON")  # PRAGMA does not persist in .db!
    # creates DB file if it did not exist prior to sqlite3.connect()
    if not db_exists or rebuild:
        with open("db/schema.sql") as f:
            conn.executescript(f.read())
        with open("db/seed.sql") as f:
            conn.executescript(f.read())

    return conn


def main() -> None:
    conn = establish_db_connection("db/library.db", rebuild=True)
    try:
        add_member(conn, "Daisy", "daisy@yahoo.com", date(2015, 12, 15))
        update_member(conn, 7, email_address="daisy2@yahoo.com")
        # delete_member(conn, 7)
        add_book_record(conn, "An Inspector Calls", "English", False)
    except Exception as e:
        print(e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
