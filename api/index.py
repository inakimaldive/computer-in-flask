from flask import Flask, render_template

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/about')
def about():
    return 'About'

@app.route('/time')
def get_time():
    from datetime import datetime
    return f"<div>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>"

@app.route('/time-page')
def time_page():
    return render_template('time.html')
