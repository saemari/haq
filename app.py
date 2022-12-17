from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questions')
def questions():
    return render_template('questions.html')

@app.route('/stats')
def stats():
    with open("poem.txt", "r", encoding='utf-8') as f:
        content = f.read().split('\n')
    return render_template("poem.html", content=content)

if __name__ == '__main__':
    app.run(debug=True)
