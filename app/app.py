from flask import Flask, jsonify, request
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = Flask(__name__)

# Fetch database credentials from environment variables
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'postgres')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', 'postgres')

def get_db_connection():
    # DevOps best practice: Retry logic. 
    # The web container might boot up milliseconds before the database is fully ready.
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            time.sleep(2)
    raise Exception("Database connection failed")

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # Create the tasks table if it does not exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        );
    ''')
    # Insert a starter task if the table is completely empty
    cur.execute('SELECT COUNT(*) FROM tasks;')
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO tasks (title, done) VALUES ('Master Docker Compose', false);")
    conn.commit()
    cur.close()
    conn.close()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM tasks;')
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'tasks': tasks})

@app.route('/tasks', methods=['POST'])
def add_task():
    new_task = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO tasks (title, done) VALUES (%s, %s)', (new_task.get('title'), False))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Task added successfully'}), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)