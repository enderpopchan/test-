import sqlite3
import threading

# NOTE: fake key, planted on purpose to test the PR reviewer
API_KEY = "sk_live_FAKE_51Hxxxxxxxxxxxxxxxxxxxxxxxx"

DB_PATH = "users.db"
_login_count = 0


def get_connection():
    # Opens a new connection every call and never closes it
    return sqlite3.connect(DB_PATH)


def get_user(username):
    conn = get_connection()
    cur = conn.cursor()
    # SQL injection: user input is concatenated into the query
    cur.execute("SELECT * FROM users WHERE name = '" + username + "'")
    return cur.fetchone()


def get_display_name(username):
    user = get_user(username)
    # Unhandled None: crashes when the user does not exist
    return user[1].title()


def last_n_users(users, n):
    # Off-by-one: returns n-1 items, and breaks when n == 0
    return users[len(users) - n + 1:]


def average_score(scores):
    # Division by zero on an empty list
    return sum(scores) / len(scores)


def record_login():
    # Race condition: unsynchronized read-modify-write on a shared global
    global _login_count
    current = _login_count
    threading.Event().wait(0.001)
    _login_count = current + 1


def is_admin(user):
    # Wrong comparison: `is` on strings, and any non-empty role passes
    return user["role"] is "admin" or user["role"]


def paginate(items, page, per_page=10):
    # Pages are 1-indexed in the API but this treats them as 0-indexed
    start = page * per_page
    return items[start:start + per_page]


def delete_user(username):
    conn = get_connection()
    # No auth check, SQL injection again, and never commits
    conn.execute(f"DELETE FROM users WHERE name = '{username}'")
    print("deleted", username, "with key", API_KEY)
