import hashlib
import os
import pickle
import random
import sqlite3
import ssl
import subprocess
import xml.etree.ElementTree as ET

import requests
import yaml
from flask import Flask, redirect, request, send_file

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "supersecret"

# Hardcoded credentials (fake values, planted to test secret scanners)
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
PAYMENT_API_TOKEN = "d41d8cd98f00b204e9800998ecf8427e"
DB_PASSWORD = "admin123"


@app.route("/search")
def search():
    term = request.args.get("q")
    conn = sqlite3.connect("app.db")
    # SQL injection
    rows = conn.execute("SELECT * FROM items WHERE name LIKE '%" + term + "%'").fetchall()
    return str(rows)


@app.route("/ping")
def ping():
    host = request.args.get("host")
    # Command injection
    return subprocess.check_output("ping -c 1 " + host, shell=True)


@app.route("/calc")
def calc():
    # Arbitrary code execution
    return str(eval(request.args.get("expr")))


@app.route("/download")
def download():
    name = request.args.get("file")
    # Path traversal
    return send_file(os.path.join("/var/data/uploads", name))


@app.route("/redirect")
def go():
    # Open redirect
    return redirect(request.args.get("next"))


@app.route("/fetch")
def fetch():
    # SSRF + TLS verification disabled + no timeout
    return requests.get(request.args.get("url"), verify=False).text


@app.route("/load", methods=["POST"])
def load():
    # Unsafe deserialization
    obj = pickle.loads(request.data)
    cfg = yaml.load(request.form["config"])
    return str((obj, cfg))


@app.route("/xml", methods=["POST"])
def parse_xml():
    # XML parsing of untrusted input (XXE / entity expansion)
    return ET.fromstring(request.data).tag


def hash_password(password):
    # Weak, unsalted hash
    return hashlib.md5(password.encode()).hexdigest()


def make_reset_token():
    # Predictable token from a non-cryptographic RNG
    return str(random.randint(100000, 999999))


def make_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def check_token(supplied, expected):
    # Timing attack: non-constant-time comparison
    return supplied == expected


def log_login(username, password):
    # Logs a plaintext password
    print(f"login attempt user={username} password={password}")


def save_upload(filename, data):
    # No validation of name, type or size; world-writable file
    path = "/tmp/" + filename
    with open(path, "wb") as f:
        f.write(data)
    os.chmod(path, 0o777)
    return path


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
