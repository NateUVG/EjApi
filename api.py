from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


# Inicio con los verbos
@app.route('/')
def inicio():
    return """
    <html>
        <head>
            <title>Documentación API de Incidentes</title>
        </head>
        <body>
            <h1>API de Gestión de Incidentes</h1>
            <table >
                <tr>
                    <th>Método</th>
                    <th>Endpoint</th>
                    <th>Descripción</th>
                </tr>
                <tr>
                    <td>POST</td>
                    <td>/incidents</td>
                    <td>Crea un nuevo incidente.</td>
                </tr>
                <tr>
                    <td>GET</td>
                    <td>/incidents</td>
                    <td>Obtiene la lista de incidentes.</td>
                </tr>
                <tr>
                    <td>GET</td>
                    <td>/incidents/{id}</td>
                    <td>Obtiene un incidente específico.</td>
                </tr>
                <tr>
                    <td>PUT</td>
                    <td>/incidents/{id}</td>
                    <td>Actualiza el estado de un incidente.</td>
                </tr>
                <tr>
                    <td>DELETE</td>
                    <td>/incidents/{id}</td>
                    <td>Elimina un incidente reportado por error.</td>
                </tr>
            </table>
        </body>
    </html>
    """
    
    

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


# Actualizar los incidentes
@app.route("/incidents/<int:id>", methods=["PUT"])
def update_incident(id):
    data = request.get_json()
    status = data.get("status")

    if status not in ["pendiente", "en proceso", "resuelto"]:
        return jsonify({"error": "Estado no válido"}), 400

    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE incidents
        SET status = ?
        WHERE id = ?
    """, (status, id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Estado actualizado exitosamente"}), 200

# Get con id de incidente
@app.route("/incidents/<int:id>", methods=["GET"])
def get_incident(id):
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents WHERE id = ?", (id,))
    incident = cursor.fetchone()
    conn.close()

    if incident:
        return jsonify(incident)
    else:
        return jsonify({"error": "Incidente no encontrado"}), 404

    
# Eliminar
@app.route("/incidents/<int:id>", methods=["DELETE"])
def delete_incident(id):
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM incidents WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Incidente eliminado exitosamente"}), 200

if __name__ == "__main__":
    app.run(debug=True)