from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Inicializar base de datos
with sqlite3.connect("incidents.db") as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reporter TEXT NOT NULL,
            description TEXT NOT NULL CHECK(length(description) >= 10),
            status TEXT DEFAULT 'pendiente',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)


if __name__ == "__main__":
    app.run(debug=True)