from flask import Flask, request, render_template, redirect, url_for, session, jsonify, flash
import sqlite3
import os
import json

DATABASE_NAME = "database.db"
app = Flask(__name__)
app.secret_key = os.urandom(24)

class DatabaseWrappers:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
    def reset_database(self):
        self.cursor.execute("DROP TABLE IF EXISTS games")
        self.conn.commit()
        
    def create_user_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)")
        
    def register_user(self, username, email, password):
        if not self.user_exists(username):
            self.cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            self.conn.commit()

    def user_exists(self, username):
        self.cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone() is not None
    
    def email_exists(self, email):
        self.cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
        return self.cursor.fetchone() is not None

    def authenticate_user(self, username, password):
        self.cursor.execute("SELECT 1 FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone() is not None
        
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY, 
                title TEXT, 
                price REAL, 
                genre TEXT, 
                images TEXT,
                publisher TEXT,
                description TEXT
            )
        """)
        self.cursor.execute("PRAGMA table_info(games)")
                    
    def game_exists(self, title):
        self.cursor.execute("SELECT 1 FROM games WHERE title = ?", (title,))
        return self.cursor.fetchone() is not None

    def add_game(self, title, price, genre, images, publisher, description):
        if not self.game_exists(title):
            self.cursor.execute("""
                INSERT INTO games (title, price, genre, images, publisher, description) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, price, genre, images, publisher, description))
            self.conn.commit()
            
    def get_game_details(self, game_id):
        self.cursor.execute("SELECT * FROM games WHERE id = ?", (game_id,))
        game = self.cursor.fetchone()
        if game is not None:
            return {
                'id': game[0], 
                'title': game[1], 
                'price': game[2], 
                'genre': game[3], 
                'images': game[4].split(", "),
                'publisher': game[5],
                'description': game[6]
            }
        else:
            return None

db = DatabaseWrappers()
db.reset_database()
db.create_table()
db.create_user_table()

# ======================================================================================== #

@app.route('/')
def index():
    current_user = session.get('username')
    return render_template('index.html', current_user=current_user)

@app.route('/missions')
def missions():
    return render_template('missions.html')

@app.route('/livestreams')
def livestreams():
    return render_template('livestreams.html')

@app.route('/cart')
def cart():
    if 'username' not in session:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not email or '@' not in email:
            flash('Invalid email')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        if db.user_exists(username) or db.email_exists(email):
            flash('Username or email already exists')
            return redirect(url_for('register'))

        db.register_user(username, email, password)
        flash('Registered successfully')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/games')
def get_games():
    db.cursor.execute("SELECT id, title, price, genre, images FROM games")
    games = db.cursor.fetchall()
    games = [[game[0], game[1], game[2], game[3].split(", "), game[4].split(", ")] for game in games]
    return jsonify(games)

@app.route('/game/<game_id>')
def game(game_id):
    game_details = db.get_game_details(game_id)
    return render_template('game.html', game=game_details)

@app.route('/search/<title>')
def search_games(title):
    db.cursor.execute("SELECT id, title, price, genre, images FROM games WHERE title LIKE ?", ('%' + title + '%',))
    games = db.cursor.fetchall()
    games = [[game[0], game[1], game[2], game[3].split(", "), game[4]] for game in games]
    return jsonify(games)

def add_games_to_database():
    with open('static/games.json') as f:
        games = json.load(f)
        for game in games:
            db.add_game(game['title'], game['price'], ', '.join(game['genre']), ', '.join(game['images']), game['publisher'], game['description'])

if __name__ == "__main__":
    add_games_to_database()
    
    app.run(debug=True)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
