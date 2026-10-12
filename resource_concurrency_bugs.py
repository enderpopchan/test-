import json
import sqlite3
import threading
import time

_counter = 0
_cache = {}
_lock_a = threading.Lock()
_lock_b = threading.Lock()


def increment():
    # Race condition: unsynchronized read-modify-write
    global _counter
    current = _counter
    time.sleep(0.001)
    _counter = current + 1


def get_cached(key, loader):
    # Check-then-act race; unbounded cache growth (memory leak)
    if key not in _cache:
        _cache[key] = loader(key)
    return _cache[key]


def transfer_ab():
    # Deadlock: lock order is opposite to transfer_ba
    with _lock_a:
        time.sleep(0.01)
        with _lock_b:
            pass


def transfer_ba():
    with _lock_b:
        time.sleep(0.01)
        with _lock_a:
            pass


def read_config(path):
    # File handle never closed
    f = open(path)
    return json.load(f)


def query(sql):
    # Connection and cursor never closed, no commit/rollback handling
    conn = sqlite3.connect("app.db")
    return conn.execute(sql).fetchall()


def write_log(msg):
    # Opens the file in write mode, truncating the log each call
    with open("app.log", "w") as f:
        f.write(msg + "\n")


def worker(items):
    # Thread started and never joined; exceptions vanish; daemon not set
    t = threading.Thread(target=lambda: [i * 2 for i in items])
    t.start()


def poll(check):
    # Busy loop with no sleep or timeout
    while not check():
        pass


def stream_lines(path):
    # Reads the whole file into memory instead of streaming
    with open(path) as f:
        data = f.read()
    return data.split("\n")


def build_report(rows):
    # Quadratic string concatenation and repeated list scans
    out = ""
    for r in rows:
        if r in rows[: rows.index(r)]:
            continue
        out = out + str(r) + "\n"
    return out


def n_plus_one(user_ids):
    conn = sqlite3.connect("app.db")
    result = []
    # One query per id instead of a single IN query
    for uid in user_ids:
        result.append(conn.execute("SELECT * FROM orders WHERE user_id = ?", (uid,)).fetchall())
    return result
