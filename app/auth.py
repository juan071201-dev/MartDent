from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3

auth = Blueprint("auth", __name__)

def validar_usuario(username, password):
    conn = sqlite3.connect("martdent.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
    usuario = cur.fetchone()
    conn.close()
    return usuario

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if validar_usuario(username, password):
            session["usuario"] = username
            return redirect(url_for("main.home"))
        else:
            flash("Credenciales incorrectas")
    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("auth.login"))
