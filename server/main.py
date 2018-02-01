from flask import Flask, render_template, request, url_for, redirect, g, session, flash
import mysql.connector
import requests
import time
import threading
from bs4 import BeautifulSoup
import datetime
import time
import random
import hashlib
import binascii
import RPi.GPIO as GPIO
import math

app = Flask(__name__)
# configure salt and set GPIO pins
salt = b'\xf5\xbb;\xd8S\xeb\x0b\xf8\xe8\xef\x9d\xab\xa1\xce<\x8c\xfeIP\xfc'
loudGPIO = 7
averageGPIO = 11
silenceGPIO = 22
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(loudGPIO, GPIO.OUT)
GPIO.setup(averageGPIO, GPIO.OUT)
GPIO.setup(silenceGPIO, GPIO.OUT)

# set the secret key for flask sessions
app.secret_key = 'some_secret'

@app.route('/', methods=['POST', 'GET'])
def main():
    # return the login page
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # compare entered password against hashed pbkdf2 password in database
        hashedPassword = (binascii.hexlify(hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000))).decode()
        classRoom = request.form['classRoom']
        db = mysql.connector.connect(user='root', password='idp',
                                      host='127.0.0.1',
                                      database='idp_project')
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT Gebruikersnaam, Wachtwoord FROM Docent;")
        for row in cursor:
            if username == row[0] and hashedPassword == row[1]:
                cursor.execute("SELECT Klas FROM Lamp;")
                # check if classroom exists else give user error message
                for schoolClassDb in cursor:
                    if schoolClassDb[0] == classRoom:
                        return redirect(url_for('overview', username=username, classRoom=classRoom))
                    else:
                        error = 'Die klas bestaat niet'
                        pass
            else:
                error = 'Gebruikersnaam of wachtwoord klopt niet'
                pass
        cursor.close()
        db.close()
    return render_template('index.html', error=error)

@app.route('/overview/<username>/<classRoom>', methods=['POST', 'GET'])
def overview(username, classRoom):
    # show the overview, user can select sensivity for sensor
    if request.method == 'POST':
        maxValue = request.form['maxValue']

        return redirect(url_for('process', username=username,classRoom=classRoom, maxValue=maxValue))
    return render_template('overview.html', username=username, classRoom=classRoom)

measurements = []
@app.route('/process/<username>/<classRoom>/<maxValue>', methods=['POST', 'GET'])
def process(username,classRoom, maxValue):
    # show the process with the dynamic table
    error = None
    if request.method == 'POST':
        # on stop measurement turn LED's of and save sessiondata in database
        GPIO.output(loudGPIO, GPIO.LOW)
        GPIO.output(averageGPIO, GPIO.LOW)
        GPIO.output(silenceGPIO,GPIO.LOW)
        # get the average measurement
        try:
            average = sum(measurements)/len(measurements)
        except ZeroDivisionError:
            return redirect(url_for('overview', username=username, classRoom=classRoom))
        starttime = session.get('starttime')
        endtime = datetime.datetime.now()
        duration = endtime - starttime
        db = mysql.connector.connect(user='root', password='idp',
                                      host='127.0.0.1',
                                      database='idp_project')
        cursor = db.cursor()
        try:
            # find themathcing  teacher and classroom in the database
            cursor.execute("SELECT DocentID FROM Docent WHERE Gebruikersnaam = %s;", (username,))
            docentID = cursor.fetchone()[0]
            cursor.execute("SELECT LampID FROM Lamp WHERE Klas = %s;", (classRoom,))
            lampID = cursor.fetchone()[0]
            cursor.execute("""INSERT INTO Sessie(Gemiddelde, Starttijd, Eindtijd, Duur, DocentID, LampID) VALUES (%s, %s, %s, %s, %s, %s);""", (average, starttime, endtime, duration, docentID, lampID))
            cursor.close()
            db.commit()
            db.close()
            return redirect(url_for('overview', username=username, classRoom=classRoom))
        except:
            error = 'Uw klas of uw naam bestaat niet, neem contact op met de beheerder'
            pass
    return render_template('process.html', maxValue=maxValue, error=error)
@app.route('/measure_values/<maxValue>')
def measure_values(maxValue):
    # get the set values from the overview.html and put them in a list
    setValues = [int(value) for value in maxValue.split(',')]
    # turn LED's off on startup
    GPIO.output(loudGPIO, GPIO.LOW)
    GPIO.output(averageGPIO, GPIO.LOW)
    GPIO.output(silenceGPIO,GPIO.LOW)
    starttime = datetime.datetime.now()
    session['starttime'] = starttime
    def generate():
        while True:
            try:
                page = requests.get('http://192.168.1.1:8080')
                soup = BeautifulSoup(page.content, 'lxml')
                found = float(soup.find('div', class_='volumeValue').text.strip())
                if math.isinf(found) == True:
                    found = 0
                    pass
                color = None
                # compare shown values against set values
                if found > setValues[1]:
                    color = 'Rood'
                elif found > setValues[0] and found < setValues[1]:
                    color = 'Geel'
                else:
                    color = 'Groen'
                # generate string with the values
                yield '{}, {},{}\n'.format(now,found,color)

                time.sleep(0.5)
                GPIO.output(loudGPIO, GPIO.LOW)
                GPIO.output(averageGPIO, GPIO.LOW)
                GPIO.output(silenceGPIO,GPIO.LOW)
                if found > setValues[1]:
                    GPIO.output(loudGPIO, GPIO.HIGH)
                elif found > setValues[0] and found < setValues[1]:
                    GPIO.output(averageGPIO, GPIO.HIGH)
                else:
                    GPIO.output(silenceGPIO, GPIO.HIGH)
                measurements.append(found)
            # on error set LED's off
            except requests.exceptions.ConnectionError:
                GPIO.output(loudGPIO, GPIO.LOW)
                GPIO.output(averageGPIO, GPIO.LOW)
                GPIO.output(silenceGPIO,GPIO.LOW)
                pass
            except:
                GPIO.output(loudGPIO, GPIO.LOW)
                GPIO.output(averageGPIO, GPIO.LOW)
                GPIO.output(silenceGPIO,GPIO.LOW)
                raise
    return app.response_class(generate())

# start the application. Threaded so multiple users can login and force https with self signed certificate
app.run('0.0.0.0', 8080, threaded=True, ssl_context=('cert.pem', 'key.pem'))
