from flask import Flask
from flask import render_template
import mysql.connector
from flask import request


app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def main():
    cnx = mysql.connector.connect(user='root', password='idp',
                                  host='127.0.0.1',
                                  database='idp_project')
    cnx.close()
    return render_template('index.html')
app.run('0.0.0.0', 8080)
