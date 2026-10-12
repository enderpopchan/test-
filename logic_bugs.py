from datetime import datetime, timedelta


def last_n(items, n):
    # Off-by-one
    return items[len(items) - n + 1:]


def average(values):
    # Division by zero on empty input
    return sum(values) / len(values)


def paginate(items, page, per_page=10):
    # 1-indexed page treated as 0-indexed
    start = page * per_page
    return items[start:start + per_page]


def is_admin(user):
    # `is` on strings; second clause makes every non-empty role admin
    return user["role"] is "admin" or user["role"]


def apply_discount(price, percent):
    # Integer division truncates; no bounds check on percent
    return price - (price * percent // 100)


def is_close(a, b):
    # Float equality
    return a + b == 0.3


def first_word(text):
    # Crashes on empty string / None
    return text.split()[0]


def get_name(user):
    # Unhandled None
    return user.get("profile").get("name").title()


def add_item(item, bucket=[]):
    # Mutable default argument shared across calls
    bucket.append(item)
    return bucket


def days_until(deadline_str):
    # Naive datetime, wrong format assumption, and ignores time zones / DST
    deadline = datetime.strptime(deadline_str, "%d/%m/%Y")
    return (deadline - datetime.now()).days


def next_week():
    # Adds 7 days to a timestamp but drops the time zone
    return datetime.utcnow() + timedelta(days=7)


def find_user(users, name):
    for u in users:
        if u["name"] == name:
            return u
        else:
            # Returns on the first non-match
            return None


def sum_to(n):
    total = 0
    # Range excludes n
    for i in range(n):
        total += i
    return total


def transfer(accounts, src, dst, amount):
    # No balance check, allows negative amounts, not atomic
    accounts[src] -= amount
    accounts[dst] += amount


def count_words(text):
    counts = {}
    for w in text.split():
        # KeyError on first occurrence
        counts[w] += 1
    return counts


def merge(a, b):
    # Mutates the caller's dict
    a.update(b)
    return a


def percent_complete(done, total):
    # Integer vs float; ZeroDivisionError
    return done / total * 100


def clamp(x, lo, hi):
    # Arguments swapped in the comparison
    return max(hi, min(x, lo))


def is_leap(year):
    # Wrong rule: ignores the 100/400 exceptions
    return year % 4 == 0


def retry(fn, attempts=3):
    for _ in range(attempts):
        try:
            return fn()
        except Exception:
            # Swallows every error, then returns None silently
            pass
