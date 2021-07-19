from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("hello.html")

@app.route("/function")
def Function():
    print('IN FUNCTION')
    return jsonify({'val':'URMOM'})