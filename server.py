import argparse
from flask import Flask, request, jsonify, render_template
import sqlite3
import os
import json

DATABASE_NAME = "database.db"
app = Flask(__name__)

class DatabaseWrappers:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, title TEXT, price REAL, genre TEXT)")
        
    def game_exists(self, title):
        self.cursor.execute("SELECT 1 FROM games WHERE title = ?", (title,))
        return self.cursor.fetchone() is not None

    def add_game(self, title, price, genre):
        if not self.game_exists(title):
            self.cursor.execute("INSERT INTO games (title, price, genre) VALUES (?, ?, ?)", (title, price, genre))
            self.conn.commit()
        

db = DatabaseWrappers()
db.create_table()

# ======================================================================================== #

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/games')
def get_games():
    db.cursor.execute("SELECT * FROM games")
    games = db.cursor.fetchall()
    games = [[game[0], game[1], game[2], game[3].split(", ")] for game in games]
    return jsonify(games)

@app.route('/search/<title>')
def search_games(title):
    db.cursor.execute("SELECT * FROM games WHERE title LIKE ?", ('%' + title + '%',))
    games = db.cursor.fetchall()
    games = [[game[0], game[1], game[2], game[3].split(", ")] for game in games]
    return jsonify(games)

with open('static/games.json') as f:
    games = json.load(f)
    for game in games:
        db.add_game(game['title'], game['price'], ', '.join(game['genre']))

if __name__ == "__main__":
    app.run(debug=True)
