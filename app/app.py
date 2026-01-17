from flask import Flask, request, jsonify
from db import get_db, init_db
from datetime import datetime

app = Flask(__name__)

init_db()

@app.route("/", methods=["GET"])
def index():
    ip = request.remote_addr
    username = "anonymous"

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, attempts FROM login_attempts
        WHERE username=? AND ip_address=?
    """, (username, ip))

    row = cur.fetchone()

    if row:
        cur.execute("""
            UPDATE login_attempts
            SET attempts = attempts + 1,
                last_attempt = ?
            WHERE id = ?
        """, (datetime.utcnow(), row["id"]))
    else:
        cur.execute("""
            INSERT INTO login_attempts (username, ip_address)
            VALUES (?, ?)
        """, (username, ip))

    conn.commit()
    conn.close()

    return "OK", 200

@app.route("/login-attempt", methods=["POST"])
def login_attempt():
    data = request.json

    username = data.get("username")
    ip = request.remote_addr

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, attempts FROM login_attempts
        WHERE username=? AND ip_address=?
    """, (username, ip))

    row = cur.fetchone()

    if row:
        cur.execute("""
            UPDATE login_attempts
            SET attempts = attempts + 1,
                last_attempt = ?
            WHERE id = ?
        """, (datetime.utcnow(), row["id"]))
    else:
        cur.execute("""
            INSERT INTO login_attempts (username, ip_address)
            VALUES (?, ?)
        """, (username, ip))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"}), 200


@app.route("/stats", methods=["GET"])
def stats():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM login_attempts ORDER BY attempts DESC")
    rows = [dict(r) for r in cur.fetchall()]

    conn.close()
    return jsonify(rows)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
