from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash, session
import os
import psycopg
from psycopg.rows import dict_row # dictionnaires 
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv #fichier .env
import re #pour les regex
from functools import wraps #Décorateur
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired  # CSRF

auth_bp = Blueprint('auth', __name__)

pseudo_regex = r'^[a-zA-Z0-9_]{3,15}$'
password_regex = r'^(?=.*\d).{8,16}$'

# ================================
#       CSRF
# ================================
def generate_csrf_token():
    """Génère un token signé et le stocke en session."""
    s = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    token = s.dumps(session.get('joueur_id', 'anonymous'))
    session['csrf_token'] = token
    return token

def verify_csrf_token(token):
    """Vérifie que le token reçu est valide et correspond à celui en session."""
    if not token:
        return False
    s = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    try:
        s.loads(token, max_age=3600)  # expire après 1h
    except (BadSignature, SignatureExpired):
        return False
    return token == session.get('csrf_token')

# ================================
#       SÉCURITÉ (Décorateur)
# ================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Si pas de session
        if 'joueur_id' not in session:
            flash("Accès refusé. Veuillez vous connecter pour jouer !", "error")
            return redirect(url_for('auth.login'))  
        # Si session
        return f(*args, **kwargs)
    return decorated_function

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
        # Vérification CSRF
        if not verify_csrf_token(request.form.get('csrf_token')):
            flash("Requête invalide, veuillez réessayer.")
            return redirect(url_for('auth.login'))

        pseudo = request.form.get('pseudo')
        password = request.form.get('password')
        con, cur = get_db_connection()

        try:
            cur.execute("SELECT * FROM users WHERE pseudo = %s", (pseudo,))
            user = cur.fetchone()
            
            # Vérification mot de passe 
            if user and check_password_hash(user['mot_de_passe'], password): 
                session['joueur_id'] = user['id']
                session['joueur_pseudo'] = user['pseudo']
                session['joueur_avatar'] = user['avatar']
                return redirect(url_for('game.podiumScreen'))
            else:
                flash("Informations invalides.")
                return redirect(url_for('auth.login'))            
        finally:
            # On ferme manuellement 
            cur.close()
            con.close()

    # token et on le passe au template
    csrf_token = generate_csrf_token()
    return render_template("index.html", csrf_token=csrf_token)

#====================
#   PAGE SIGN-IN
#====================
@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Vérification CSRF
        if not verify_csrf_token(request.form.get('csrf_token')):
            flash("Requête invalide, veuillez réessayer.")
            return redirect(url_for('auth.signin'))

        pseudo = request.form.get('pseudo')
        password = request.form.get('password')
        avatar = request.form.get('avatar')

        if not re.match(pseudo_regex, pseudo):
            flash("Le pseudo doit faire entre 3 et 15 caractères (sans espaces et caractères spéciaux).")
            return redirect(url_for('auth.signin'))
        if not re.match(password_regex, password):
            flash("Le mot de passe doit faire entre 8 et 16 caractères et contenir au moins un chiffre.")
            return redirect(url_for('auth.signin'))
        
        hashed_password = generate_password_hash(password)
        con, cur = get_db_connection()

        try:
            # Insertion données
            cur.execute(
                "INSERT INTO users (pseudo, mot_de_passe, avatar) VALUES (%s, %s, %s) RETURNING id", 
                (pseudo, hashed_password, avatar)
            )
            #reprendre l'id du nouveau users
            new_user = cur.fetchone()
            user_id = new_user['id']
            con.commit() 

            session['joueur_id'] = user_id
            session['joueur_pseudo'] = pseudo  
            session['joueur_avatar'] = avatar

            flash("Compte créé avec succès ! Bienvenue.")

            return redirect(url_for('game.podiumScreen'))
            
        except psycopg.IntegrityError:
            # souci : rollback 
            con.rollback() 
            flash("L'inscription a échoué : cet pseudo est déjà utilisé.")
            return redirect(url_for('auth.signin'))
            
        finally:
            cur.close()
            con.close() # Fermeture manuel

    #GET (Chargement normal de la page)
    avatar_dir = os.path.join(current_app.static_folder, 'ASSETS', 'IMAGES', 'iconProfil')
    try:
        avatars = [f for f in os.listdir(avatar_dir) if f.endswith('.png')]
        avatars.sort(key=lambda x: int(x.split('.')[0])) 
    except FileNotFoundError:
        avatars = []

    # GET : on génère un token et on le passe au template
    csrf_token = generate_csrf_token()
    return render_template('signin.html', avatars=avatars, csrf_token=csrf_token)

#====================
#   PAGE SIGN-OUT
#====================
@auth_bp.route('/logout')
def logout():
    session.clear() 
    flash("Vous avez été déconnecté avec succès.")
    return redirect(url_for('auth.login'))

#====================
#   OPTIONS
#====================
@auth_bp.route('/options', methods=['GET', 'POST']) 
@login_required
def optionScreen():
    if request.method == 'POST':
        # Vérification CSRF
        if not verify_csrf_token(request.form.get('csrf_token')):
            flash("Requête invalide, veuillez réessayer.")
            return redirect(url_for('auth.optionScreen'))

        new_pseudo = request.form.get('new_pseudo')
        joueur_id = session.get('joueur_id')

        if not re.match(pseudo_regex, new_pseudo):
            flash("Le pseudo doit faire entre 3 et 15 caractères (sans espaces ni caractères spéciaux).")
            return redirect(url_for('auth.optionScreen'))

        con, cur = get_db_connection()
        try:
            cur.execute("UPDATE users SET pseudo = %s WHERE id = %s", (new_pseudo, joueur_id))
            con.commit()

            session['joueur_pseudo'] = new_pseudo  
            flash("Votre pseudo a été mis à jour avec succès !")
            
        except psycopg.IntegrityError:
            con.rollback()
            flash("Ce pseudo est déjà utilisé par un autre traqueur !")
        finally:
            cur.close()
            con.close()

        return redirect(url_for('auth.optionScreen')) 

    # GET on génère un token et on le passe au template
    csrf_token = generate_csrf_token()
    return render_template('options.html', csrf_token=csrf_token)