from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash
import os
import psycopg
from psycopg.rows import dict_row # dictionnaires 
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv #fichier .env
import re #pour les regex

auth_bp = Blueprint('auth', __name__)

#====================
#   CONNEXION DB
#====================
def get_db_connection():
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    conn_info = f"dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}"

    con = psycopg.connect(conn_info, row_factory=dict_row)
    cur = con.cursor()
    return con, cur

#====================
#   PAGE LOGIN
#====================
@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('login')
        password = request.form.get('password')
        con, cur = get_db_connection()

        try:
            cur.execute("SELECT * FROM joueurs WHERE email = %s", (email,))
            user = cur.fetchone()
            
            # Vérification mot de passe 
            if user and check_password_hash(user['mot_de_passe'], password): 
                return redirect(url_for('game.gameScreen'))
            else:
                flash("Informations invalides.")
                return redirect(url_for('auth.login'))            
        finally:
            # On ferme manuellement (le prof il veut)
            cur.close()
            con.close()
    return render_template("index.html")

#====================
#   PAGE SIGN-IN
#====================
@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('login')
        password = request.form.get('password')
        avatar = request.form.get('avatar')
        email_regex = r'^[^@]+@[^@]+\.[^@]+$'
        password_regex = r'^(?=.*\d).{8,16}$'

        if not re.match(email_regex, email):
            flash("Format d'email invalide.")
            return redirect(url_for('auth.signin'))
        if not re.match(password_regex, password):
            flash("Le mot de passe doit faire entre 8 et 16 caractères et contenir au moins un chiffre.")
            return redirect(url_for('auth.signin'))
        
        hashed_password = generate_password_hash(password)
        con, cur = get_db_connection()

        try:
            # Insertion données
            cur.execute(
                "INSERT INTO joueurs (email, mot_de_passe, avatar) VALUES (%s, %s, %s)", 
                (email, hashed_password, avatar)
            )
            # commit "prof=> toujours a la connection gnagnagna"
            con.commit() 
            return redirect(url_for('auth.login'))
            
        except psycopg.IntegrityError:
            # souci : rollback 
            con.rollback() 
            flash("L'inscription a échoué : cet email est déjà utilisé.")
            return redirect(url_for('auth.signin'))
            
        finally:
            cur.close()
            con.close() # Fermeture manuel

    # --- PARTIE GET (Chargement normal de la page) ---
    avatar_dir = os.path.join(current_app.static_folder, 'ASSETS', 'IMAGES', 'iconProfil')
    try:
        avatars = [f for f in os.listdir(avatar_dir) if f.endswith('.png')]
        avatars.sort(key=lambda x: int(x.split('.')[0])) 
    except FileNotFoundError:
        avatars = []
        
    return render_template('signin.html', avatars=avatars)