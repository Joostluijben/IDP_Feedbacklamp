from flask import Flask
from flask import render_template
from hey import readAudio
app = Flask(__name__)
@app.route('/')
def main():
    return render_template('index.html', value=readAudio())
app.run('0.0.0.0', 8080)
