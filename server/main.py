from flask import Flask, render_template, request, url_for, redirect, g, session, flash
import mysql.connector
import requests
import time
import threading
import requests
from bs4 import BeautifulSoup
import datetime
import time
from functools import wraps
import random
import hashlib
import binascii
import RPi.GPIO as GPIO

app = Flask(__name__)
salt = b'\xf5\xbb;\xd8S\xeb\x0b\xf8\xe8\xef\x9d\xab\xa1\xce<\x8c\xfeIP\xfc'
loudGPIO = 7
averageGPIO = 11
silenceGPIO = 22
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(loudGPIO, GPIO.OUT)
GPIO.setup(averageGPIO, GPIO.OUT)
GPIO.setup(silenceGPIO, GPIO.OUT)

app.secret_key = 'some_secret'

@app.route('/', methods=['POST', 'GET'])
def main():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
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
    if request.method == 'POST':
        maxValue = request.form['maxValue']

        return redirect(url_for('process', username=username,classRoom=classRoom, maxValue=maxValue))
    return render_template('overview.html', username=username, classRoom=classRoom)

measurements = []
@app.route('/process/<username>/<classRoom>/<maxValue>', methods=['POST', 'GET'])
def process(username,classRoom, maxValue):
    error = None
    if request.method == 'POST':
        GPIO.output(loudGPIO, GPIO.LOW)
        GPIO.output(averageGPIO, GPIO.LOW)
        GPIO.output(silenceGPIO,GPIO.LOW)
        try:
            average = sum(measurements)/len(measurements)
        except ZeroDivisionError:
            return redirect(url_for('overview', username=username, classRoom=classRoom))
        starttime = session.get('starttime')
        endtime = datetime.datetime.now()
        db = mysql.connector.connect(user='root', password='idp',
                                      host='127.0.0.1',
                                      database='idp_project')
        cursor = db.cursor()
        try:
            cursor.execute("SELECT DocentID FROM Docent WHERE Gebruikersnaam = %s;", (username,))
            docentID = cursor.fetchone()[0]
            cursor.execute("SELECT LampID FROM Lamp WHERE Klas = %s;", (classRoom,))
            lampID = cursor.fetchone()[0]
            cursor.execute("""INSERT INTO Sessie(Gemiddelde, Starttijd, Eindtijd, DocentID, LampID) VALUES (%s, %s, %s, %s, %s);""", (average, starttime, endtime, docentID, lampID))
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

    setValues = [int(value) for value in maxValue.split(',')]
    print(setValues)
    GPIO.output(loudGPIO, GPIO.LOW)
    GPIO.output(averageGPIO, GPIO.LOW)
    GPIO.output(silenceGPIO,GPIO.LOW)
    starttime = datetime.datetime.now()
    session['starttime'] = starttime

    def generate():
        while True:
            try:
                page = requests.get('https://192.168.1.27:8080')
                soup = BeautifulSoup(page.content, 'lxml')
                found = float(soup.find('div', class_='volumeValue').text.strip())
                color = None
                #found = random.randrange(1,11)
                now = datetime.datetime.now().strftime('%H:%M:%S %Y-%m-%d')
                if found > setValues[1]:
                    color = 'Rood'
                elif found > setValues[0] and found < setValues[1]:
                    color = 'Geel'
                else:
                    color = 'Groen'
                yield '{}, {},{}\n'.format(now,found,color)

                time.sleep(5)
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
            except requests.exceptions.ConnectionError:
                GPIO.output(loudGPIO, GPIO.LOW)
                GPIO.output(averageGPIO, GPIO.LOW)
                GPIO.output(silenceGPIO,GPIO.LOW)
                raise
            except:
                GPIO.output(loudGPIO, GPIO.LOW)
                GPIO.output(averageGPIO, GPIO.LOW)
                GPIO.output(silenceGPIO,GPIO.LOW)
                raise
    return app.response_class(generate())


app.run('0.0.0.0', 8080, debug=True, threaded=True, ssl_context=('cert.pem', 'key.pem'))
