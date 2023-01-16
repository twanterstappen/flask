import mysql.connector

import subprocess

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for, flash
)

bp = Blueprint('auth', __name__) # url_prefix='/auth' for in the blueprint


@bp.route('/login', methods=('GET', 'POST'))
def login():
    flashname = 0
    flashticketnumber = 0
    error = None
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
        query = "SELECT CONCAT_WS(' ', Passenger.firstname, Passenger.prefix, Passenger.lastname) AS Name, Ticket.ticketnumber, Flight.flightnumber, Flight.destination FROM Ticket " \
                "INNER JOIN Passenger ON Ticket.passenger_id = Passenger.id " \
                "INNER JOIN Flight ON Ticket.flight_id = Flight.id " \
                "WHERE CONCAT_WS(' ', Passenger.firstname, Passenger.prefix, Passenger.lastname) = %s and Ticket.ticketnumber = %s;"
        param = (name, ticketnumber)
        cursor.execute(query, param)
        entry = cursor.fetchone()
        
        if not entry:
            session.clear()
            query = "SELECT CONCAT_WS(' ', Passenger.firstname, Passenger.prefix, Passenger.lastname) AS Name FROM Passenger WHERE CONCAT_WS(' ', Passenger.firstname, Passenger.prefix, Passenger.lastname) = %s;"
            param = (name,)
            cursor.execute(query, param)
            entryname = cursor.fetchone()
            if not entryname:
                flashname = 1
            
   
            query = "SELECT Ticket.ticketnumber FROM Ticket WHERE Ticket.ticketnumber = %s;"
            param = (ticketnumber,)
            cursor.execute(query, param)
            entryticketnumber = cursor.fetchone()
            if not entryticketnumber:
                flashticketnumber = 1
            if flashname == 1 and flashticketnumber == 1:
                flash("Name and Ticketnumber not right!", "danger")
            elif flashname == 1:
                flash("Name not right!", "danger")
            elif flashticketnumber == 1:
                flash("Ticketnumber not right!", "danger")
            else:
                flash("Error login!", "danger")
            connectie.close() 
            return render_template('login.html')
                     
        # check if something returned
        if entry:
            connectie.close() 
            ipaddr = request.remote_addr
            session['name'] = name
            session['ticketnumber'] = ticketnumber
            session['flightnumber'] = entry[2]
            session['destination'] = entry[3]
            flash("Successfully logged in!", "success")
            try:
                subprocess.call(["sudo", "ipset", "add", "ip-whitelist", ipaddr])
            except:
                None
            return redirect(url_for('home'))
    return render_template('login.html')


@bp.route('/logout')
def logout():
    ipaddr = request.remote_addr
    try:
        subprocess.call(["sudo", "ipset", "del", "ip-whitelist", ipaddr])
    except:
        None
    session.clear()
    return redirect(url_for('auth.login'))
