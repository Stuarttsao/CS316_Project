# flask backend for web app

from flask import Flask, render_template, request, redirect, url_for, session

# simple web page with a search bar

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)