from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")# quand on se rend à cet url la fonction en dessous s'execute
def hello_world():# fonction executé au lancement
    return render_template("index.html")# renvoie sur la page index.html

if __name__ == '__main__':
    app.run(debug=True)