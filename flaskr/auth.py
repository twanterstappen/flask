import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = 'CHANGEME'

        if user is None:
            error = 'Incorrect username.'
        elif not 'CHANGEME' == 'CHANGEME':
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_username'] = 'test'
            session['user_password'] = password

            return redirect(url_for('test'))

        flash(error)

    return render_template('login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = 'CHANGME'

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))