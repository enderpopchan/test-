import os, sys, json, re
from math import *

DEBUG = True
list = [1, 2, 3]  # shadows a builtin


class manager:
    def __init__(self, a, b, c, d, e, f, g, h):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h

    def do(self, x):
        # Deeply nested, magic numbers, no docstring
        if x:
            if x > 0:
                if x < 100:
                    if x % 2 == 0:
                        return x * 3.14159 * 86400
                    else:
                        return x * 3.14159 * 3600
        return 0

    def process(self, data):
        try:
            result = json.loads(data)
        except:
            # Bare except hides every error, including KeyboardInterrupt
            pass
        return result  # UnboundLocalError if parsing failed


def unreachable():
    return 1
    print("never runs")


def duplicated_a(items):
    out = []
    for i in items:
        if i is not None:
            out.append(i.strip().lower())
    return out


def duplicated_b(items):
    out = []
    for i in items:
        if i is not None:
            out.append(i.strip().lower())
    return out


def long_function(x):
    # TODO: refactor this
    a = x + 1
    b = a + 1
    c = b + 1
    d = c + 1
    e = d + 1
    f = e + 1
    return a + b + c + d + e + f


def compare(a, b):
    # `== None`, `== True`, and a redundant else after return
    if a == None:
        return False
    if b == True:
        return True
    else:
        return False


def get_env():
    # Crashes when the variable is unset and the type is wrong (string, not int)
    return os.environ["PORT"] + 1


def wrong_types(name: int) -> str:
    # Type annotations contradict the implementation
    return len(name)


def unused(x):
    y = x * 2
    z = re.compile("abc")
    return x
