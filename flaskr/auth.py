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
        query = "SELECT CONCAT_WS(' ', Passenger.firstname, Passenger.prefix, Passenger.lastname) as Name, Ticket.ticketnumber, Flight.flightnumber, Flight.destination FROM Ticket " \
                "INNER JOIN Passenger on ticket.passenger_id = Passenger.id " \
                "INNER JOIN Flight on ticket.flight_id = Flight.id " \
                "where CONCAT_WS(' ', Passenger.firstname, Passenger.prefix, Passenger.lastname) = %s and ticketnumber = %s;"
        param = (name, ticketnumber)
        cursor.execute(query, param)
        entry = cursor.fetchone()
        connectie.close()

        # check if something returned
        print(entry)
        if entry:
            ipaddr = request.remote_addr
            session['name'] = name
            session['ticketnumber'] = ticketnumber
            session['flightnumber'] = entry[2]
            session['destination'] = entry[3]
            try:
                subprocess.call(["sudo", "ipset", "add", "ip-whitelist", ipaddr])
            except:
                return redirect(url_for('home'))
            return redirect(url_for('home'))
        else:
            session.clear()
    return render_template('login.html')


@bp.route('/logout')
def logout():
    ipaddr = request.remote_addr
    try:
        subprocess.call(["sudo", "ipset", "del", "ip-whitelist", ipaddr])
    except:
        session.clear()
        return redirect(url_for('home'))
    session.clear()
    return redirect(url_for('home'))
