from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<page>')
def load_page(page):
    return render_template(page)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
              (name, email, message))
    conn.commit()
    conn.close()

    return redirect('/contact.html')

@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    data = c.fetchall()
    conn.close()
    return str(data)

import os

init_db()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

