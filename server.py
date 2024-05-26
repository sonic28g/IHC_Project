from flask import Flask, request, render_template, redirect, url_for, session, jsonify, flash, send_from_directory
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
        self.cursor.execute("DROP TABLE IF EXISTS users")
        self.conn.commit()
        
    def create_user_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT, image TEXT)")
        
    def update_user(self, username, email, image):
        self.cursor.execute("UPDATE users SET email = ?, image = ? WHERE username = ?", (email, image, username))
        self.conn.commit()
            
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
                description TEXT,
                livestream TEXT,
                requirements TEXT,
                agerating TEXT,
                platform TEXT,
                specialistanalysis TEXT,
                rating REAL
            )
        """)
        self.cursor.execute("PRAGMA table_info(games)")
                    
    def game_exists(self, title):
        self.cursor.execute("SELECT 1 FROM games WHERE title = ?", (title,))
        return self.cursor.fetchone() is not None

    def add_game(self, title, price, genre, images, publisher, description, livestream, requirements, agerating, platform, specialistanalysis, rating):
        if not self.game_exists(title):
            self.cursor.execute("""
                INSERT INTO games (title, price, genre, images, publisher, description, livestream, requirements, agerating, platform, specialistanalysis, rating) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, price, genre, ', '.join(images), publisher, description, livestream, str(requirements), agerating, platform, specialistanalysis, rating))
            self.conn.commit()
            
    def get_game_details(self, game_id):
        self.cursor.execute("SELECT * FROM games WHERE id = ?", (game_id,))
        game = self.cursor.fetchone()
        print(game)
        if game is not None:
            return {
                'id': game[0], 
                'title': game[1], 
                'price': game[2], 
                'genre': game[3], 
                'images': game[4].split(", "),
                'publisher': game[5],
                'description': game[6],
                'livestream': game[7],
                'requirements': game[8].split(", "),
                'agerating': game[9],
                'platform': game[10],
                'specialistanalysis': game[11],
                'rating': game[12]
            }
        else:
            return None
        
    def get_all_livestreams(self):
        self.cursor.execute("SELECT id, title, images, livestream FROM games")
        livestreams = self.cursor.fetchall()
        return [{'id': livestream[0], "thumbnail": livestream[2].split(", ")[1], 'title': livestream[1], 'url': livestream[3]} for livestream in livestreams]
    
    def get_livestreams_for_game(self, game_id):
        self.cursor.execute("SELECT id, title, images, livestream FROM games  WHERE id = ?", (game_id,))
        livestreams = self.cursor.fetchall()
        return [{'id': livestream[0], "thumbnail": livestream[2].split(", ")[1], 'title': livestream[1], 'url': livestream[3]} for livestream in livestreams]
    
    def get_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()

db = DatabaseWrappers()
db.create_table()
db.create_user_table()

# ======================================================================================== #

@app.route('/')
def index():
    current_user = session.get('username')
    return render_template('index.html', current_user=current_user)

@app.route('/home')
def home():
    current_user = session.get('username')
    return render_template('home.html', current_user=current_user)

@app.route('/missions')
def missions():
    current_user = session.get('username')
    return render_template('missions.html', current_user=current_user)

@app.route('/quiz1')
def quiz1():
    current_user = session.get('username')
    return render_template('quiz1.html', current_user=current_user)

@app.route('/quiz2')
def quiz2():
    current_user = session.get('username')
    return render_template('quiz2.html', current_user=current_user)

@app.route('/livestreams')
def livestreams():
    current_user = session.get('username')
    return render_template('livestreams.html', current_user=current_user)

@app.route('/get_livestreams')
def get_livestreams():
    livestreams = db.get_all_livestreams()
    return jsonify(livestreams)

@app.route('/get_livestreams_for_game/<game_id>')
def get_livestreams_for_game(game_id):
    livestream = db.get_livestreams_for_game(game_id)
    if livestream is not None:
        return jsonify(livestream)
    else:
        return jsonify({'error': 'No livestream found for this game'}), 404

@app.route('/cart')
def cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        current_user = session.get('username')
        cart_item = session.get('cart', [])
    return render_template('cart.html', current_user=current_user, cart_item=cart_item)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        current_user = db.get_user(username)
        return render_template('profile.html', current_user=current_user)
    else:
        return redirect(url_for('login'))
    
@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'username' in session:
        username = session['username']
        email = request.form['email']
        image = request.files['image']
        
        if not image.filename.lower().endswith('.png'):
            flash('Apenas imagens PNG são permitidas')
            return redirect(url_for('profile'))

        image_path = os.path.join('static/images', image.filename)
        image.save(image_path)
        db.update_user(username, email, image_path)
        flash('Perfil atualizado com sucesso')
        return redirect(url_for('profile'))
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
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/profile_images/<path:filename>')
def profile_image(filename):
    return send_from_directory(app.config['profile_images'], filename)

@app.route('/games')
def get_games():
    db.cursor.execute("SELECT id, title, price, genre, images FROM games")
    games = db.cursor.fetchall()
    games = [[game[0], game[1], game[2], game[3].split(", "), game[4].split(", ")] for game in games]
    return jsonify(games)

@app.route('/payment')
def payment():
    current_user = session.get('username')
    return render_template('payment.html', current_user=current_user)

@app.route('/game/<game_id>')
def game(game_id):
    game_details = db.get_game_details(game_id)
    current_user = session.get('username')
    return render_template('game.html', current_user=current_user, game=game_details)

@app.route('/search/<title>')
def search_games(title):
    db.cursor.execute("SELECT id, title, price, genre, images FROM games WHERE title LIKE ?", ('%' + title + '%',))
    games = db.cursor.fetchall()
    games = [[game[0], game[1], game[2], game[3].split(", "), game[4]] for game in games]
    return jsonify(games)

@app.route('/add_to_cart/<game_id>', methods=['POST'])
def add_to_cart(game_id):
    if 'cart' not in session:
        session['cart'] = []
    game_details = db.get_game_details(game_id)
    if game_details:
        cart = session['cart']
        for i in cart:
            if i['id'] == int(game_id):
                i['quantity'] += 1
                session['cart'] = cart
                return "Item already in cart. Increased quantity", 200
        game_details['quantity'] = 1
        cart.append(game_details)
        session['cart'] = cart
        return "Item adicionado ao carrinho com sucesso!", 200
    else:
        flash('Falha ao adicionar item ao carrinho!', 'error')

@app.route('/get_cart_items')
def get_cart_items():
    if 'cart' in session:
        cartItem = session['cart']
        return jsonify(cartItem)
    else:
        return jsonify([])
    
# ======================================================================================== #

if __name__ == "__main__":    
    with open('static/games.json', 'r', encoding='utf-8') as f:
        games = json.load(f)
        for game in games:
            db.add_game(
                game['title'], 
                game['price'], 
                ', '.join(game['genre']),
                game['images'], 
                game['publisher'], 
                game['description'], 
                game['livestream'], 
                game['requirements'], 
                game['agerating'], 
                game['plataform'], 
                game['specialistanalysis'], 
                game['rating']
            )
            
    app.run(debug=True)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
