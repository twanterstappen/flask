import os

from flask import Flask, g, redirect, render_template, session, url_for

from . import auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(auth.bp)
    app.secret_key = 'CHANGEME'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def home():
        if 'name' in session:
            # Get the username from the session
            g.name = session['name']
            g.ticketnumber = session['ticketnumber']
            # Show the protected page, with the username
            return render_template('home.html')
        else:
            # Show the login page
            return redirect(url_for('auth.login'))

    @app.route('/about-us')
    def aboutus():
        return render_template('about-us.html')

    @app.route('/terms-of-use')
    def termsofuse():
        return render_template('terms-of-use.html')

    @app.route('/multimedia')
    def multimedia():
        return render_template('multimedia.html')

    #   KIJKEN  OF NODIG IS KAN VERWEIDEREN.
    @app.route('/welcome')
    def welcome():
        if 'name' in session:
            # Get the username from the session
            g.name = session['name']
            g.ticketnumber = session['ticketnumber']
            # Show the protected page, with the username
            return render_template('welcome.html')
        else:
            # Show the login page
            return redirect(url_for('auth.login'))

    return app
