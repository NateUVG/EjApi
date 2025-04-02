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


# Creamos los endpoints

#Obtener todos los incidentes
@app.route("/incidents", methods=["GET"])
def get_incidents():
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents")
    incidents = cursor.fetchall()
    conn.close()

    return jsonify(incidents)

#Crear un incidente
@app.route("/incidents", methods=["POST"])
def create_incident():
    data = request.get_json()
    reporter = data.get("reporter")
    description = data.get("description")
    status = data.get("status")
    # Validaciones
    if not reporter or len(description) < 10:
        return jsonify({"error": "La descripción es muy corta, debe ser mayor a 10 caracteres"}), 400

    # Conectar a la base de datos y ejecutar un insert
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO incidents (reporter, description, status)
        VALUES (?, ?, ?)
    """, (reporter, description, status))
    
    conn.commit()
    conn.close()

    return jsonify({"message": "Incidente creado exitosamente"}), 201


if __name__ == "__main__":
    app.run(debug=True)