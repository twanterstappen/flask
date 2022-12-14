import functools

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        name = request.form['name']
        ticketnumber = request.form['ticketnumber']

        session['name'] = name
        session['ticketnumber'] = ticketnumber
        return redirect(url_for('test'))




    return render_template('login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    # if user_id is None:
    #     g.usert = 'Hello'
    # else:
    #     g.usert = 'CHANGME'

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))



