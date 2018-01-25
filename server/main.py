from flask import Flask
from flask import render_template
import mysql.connector
from flask import request
from flask import flash
from flask import url_for, redirect
import requests
import time
import queue
import threading
import requests
from bs4 import BeautifulSoup
import datetime
import time


app = Flask(__name__)
app.secret_key = 'some_secret'


def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            time.sleep(2)
            print('In start loop')
            try:
                r = requests.get('http://127.0.0.1:8080/')
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')

    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()


q = queue.Queue()

@app.before_first_request
def runJob():
    def checkClient(q):
        while True:
            try:
                page = requests.get('http://192.168.1.25:8080/')
                soup = BeautifulSoup(page.text, 'html.parser')
                value = soup.find('div', class_='volumeValue').text.strip()
                print(value)
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(now)
                q.put([value,now])

                db = mysql.connector.connect(user='root', password='idp',
                                              host='127.0.0.1',
                                              database='idp_project')
                cursor = db.cursor(buffered=True)
                #cursor.execute("INSERT INTO Sensor (Decibel, Tijd) VALUES (%s, %s);", (value, now))
                db.commit()
                cursor.close()
                db.close()
                time.sleep(5)
            except requests.exceptions.ConnectionError:
                q.put(['Error'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                print('Cannot connect to server retrying in 5 seconds')
                time.sleep(5)
                pass


    t1 = threading.Thread(target=checkClient, name=checkClient, args=(q,))
    t1.start()


@app.route('/', methods=['POST', 'GET'])
def main():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = mysql.connector.connect(user='root', password='idp',
                                      host='127.0.0.1',
                                      database='idp_project')
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT Gebruikersnaam, Wachtwoord FROM Docent")
        for row in cursor:
            if username == row[0] and password == row[1]:
                return redirect(url_for('overview', username=username))
            else:
                error = 'Gebruikersnaam of wachtwoord klopt niet'
                pass
        cursor.close()
        db.close()
    return render_template('index.html', error=error)


@app.route('/overview/<username>', methods=['GET', 'POST'])
def overview(username):
    while True:
        value = q.get()
        db = mysql.connector.connect(user='root', password='idp',
                                      host='127.0.0.1',
                                      database='idp_project')
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT * FROM Sensor")
        rows = []
        for row in cursor:
            rows.append((row[0], row[1], row[2]))
        cursor.close()
        db.close()
        return render_template('overview.html', username=username, value=value, rows=rows)
    return render_template('overview.html', username=username)

#start_runner()
app.run('0.0.0.0', 8080, debug=True, threaded=True)
