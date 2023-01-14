# Imports
import os

from flask import Flask, g, redirect, render_template, session, url_for

from . import auth

# Function to craete and configure the app.
def create_app(test_config=None):
    # create and configure the app.
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(auth.bp)
    app.secret_key = 'CHANGEME'

    if test_config is None:
        # load the instance config, if it exists, when not testing.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in.
        app.config.from_mapping(test_config)

    # ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Home page after user logged in.
    @app.route('/')
    def home():
        if 'name' in session:
            # Get the username from the session.
            g.name = session['name']
            g.ticketnumber = session['ticketnumber']
            g.flightnumber = session['flightnumber']
            g.destination = session['destination']
            # Show the protected page, with the username.
            return render_template('home.html')
        else:
            # Show the login page
            return redirect(url_for('auth.login'))

    # Specific route will return a given html page.
    @app.route('/about-us')
    def aboutus():
        return render_template('about-us.html')

    @app.route('/terms-of-use')
    def termsofuse():
        return render_template('terms-of-use.html')

    @app.route('/multimedia')
    def multimedia():
        g.destination = session['destination']
        return render_template('multimedia.html')

    return app