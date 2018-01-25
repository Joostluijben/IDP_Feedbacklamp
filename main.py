from flask import Flask
from flask import render_template
app = Flask(__name__)
app.TEMPLATES_AUTO_RELOAD = True
@app.route('/')
def main():
    return render_template('index.html')
app.run('0.0.0.0', 8080)
