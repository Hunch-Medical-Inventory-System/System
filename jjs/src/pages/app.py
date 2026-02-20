from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

# Use environment variables instead of hardcoding creds
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": 3306
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/inventory", methods=["GET"])
def get_inventory():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM inventory;")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)