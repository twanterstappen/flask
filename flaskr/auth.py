import mysql.connector

import subprocess

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('auth', __name__) # url_prefix='/auth' for in the blueprint


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        name = request.form['name']
        ticketnumber = request.form['ticketnumber']

        connectie = mysql.connector.connect(
            host="localhost",
            database="Login",
            user="user_database",
            password="Welkom123!"
        )
        cursor = connectie.cursor()
        query = "SELECT name, ticketnumber FROM Login WHERE name = %s and ticketnumber = %s"
        param = (name, ticketnumber)
        cursor.execute(query, param)
        entry = cursor.fetchone()
        connectie.close()

        # check if something returned
        if entry:
            ipaddr = request.remote_addr
            session['name'] = name
            session['ticketnumber'] = ticketnumber
            try:
                subprocess.call(["sudo", "ipset", "add", "ip-whitelist", ipaddr])
            except:
                return redirect(url_for('home'))
            return redirect(url_for('home'))
        else:
            session.clear()
    return render_template('login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))