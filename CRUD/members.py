"""
TODO
validation for data types since SQLite has type affinity only!

Should DOB be a datetime.date object? - yyyy-mm-dd format
Use regex for email validation - import from a utils/ module.
Check type hinting notes to see if I can create a type hint
based on the regex validating email function.
"""
import sqlite3


def add_member(conn: sqlite3.Connection,
               name: str,
               email_address: str,
               date_of_birth: str,
               membership_start_date: str | None = None
               ) -> None:

    # Using a dict like this means I can allow the SQL schema default
    # values to apply in the case the Python function is called without
    # an argument being passed for the field. Otherwise, I would need to
    # have IF/ELSE conditions with similiar INSERT commands bar one field
    # depending on whether a non-default arg was passed or not.
    fields = {
        "name": name,
        "email_address": email_address,
        "date_of_birth": date_of_birth
    }
    if membership_start_date is not None:
        fields["membership_start_date"] = membership_start_date

    columns = ", ".join(fields.keys())
    placeholders = ", ".join(["?"] * len(fields))

    try:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO members ({columns}) VALUES ({placeholders})",
            tuple(fields.values())
            )
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()  # redundant for one INSERT but good practice


def update_member(conn: sqlite3.Connection,
                  member_id: int,
                  name: str | None = None,
                  email_address: str | None = None
                  ) -> None:
    """
    DOB and start date are static for member records
    """
    if name is None and email_address is None:
        raise ValueError("At least one field needs updating "
                         "(name, email_address)")

    fields = {}
    if name is not None:
        fields["name"] = name
    if email_address is not None:
        fields["email_address"] = email_address

    # f-strings can be used for fixed variables defined inside the function
    # since no risk of SQLi.
    set_condition = ", ".join(f"{col} = ?" for col in fields.keys())
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE members SET {set_condition} WHERE member_id = ?",
            (*fields.values(), member_id,)
            )
        # cursor.rowcount() reveals how many rows were effected by
        # the previous statement.
        if cursor.rowcount == 0:
            print(f"No member found with ID {member_id}")
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()


def delete_member(conn: sqlite3.Connection, member_id: int) -> None:
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM members WHERE member_id = ?",
                       (member_id,))
        if cursor.rowcount == 0:
            print(f"No member found with ID {member_id}")
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
