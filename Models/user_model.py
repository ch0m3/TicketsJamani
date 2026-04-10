from database.db import get_db_connection


def create_user(name, email, password, role):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
        (name, email, password, role)
    )
    conn.commit()
    conn.close()


def find_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()
    conn.close()
    return user


def count_cms():
    conn = get_db_connection()
    count = conn.execute(
        "SELECT COUNT(*) FROM users WHERE role = 'CM'"
    ).fetchone()[0]
    conn.close()
    return count