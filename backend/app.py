from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from werkzeug.security import check_password_hash

app = Flask(__name__)
CORS(app)

# Conexión DB
def get_db_connection():
    return mysql.connector.connect(
        host="db",  # <-- agrega la coma aquí
        user="root",
        password="12345",
        database="mastercook_db"
    )

@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    nombre = data.get("nombre")
    apellidos = data.get("apellidos")
    correo = data.get("correo")
    contrasena = data.get("password")

    if not all([nombre, apellidos, correo, contrasena]):
        return jsonify({"message": "Faltan campos obligatorios"}), 400

    nombre_completo = f"{nombre} {apellidos}"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Usuario WHERE correo = %s", (correo,))
        if cursor.fetchone():
            return jsonify({"message": "El correo ya está registrado"}), 409

        cursor.execute("""
            INSERT INTO Usuario (nombre_completo, correo, contrasena)
            VALUES (%s, %s, %s)
        """, (nombre_completo, correo, contrasena))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Registro exitoso"}), 201

    except mysql.connector.Error as err:
        print(err)
        return jsonify({"message": "Error en el servidor"}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data.get("correo")
    contrasena = data.get("contrasena")

    if not correo or not contrasena:
        return jsonify({"message": "Faltan campos obligatorios"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Usuario WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        # Comparación directa (sin hash)
        if usuario and usuario["contrasena"] == contrasena:
            return jsonify({"message": "Login exitoso", "usuario": usuario["nombre_completo"]}), 200
        else:
            return jsonify({"message": "Correo o contraseña incorrectos"}), 401

    except Exception as err:
        print("ERROR EN LOGIN:", err)
        return jsonify({"message": "Error en el servidor"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)