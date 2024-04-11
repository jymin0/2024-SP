from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

@app.route('/')
def timetable():
    return render_template("timetable.html")

if __name__ == '__main__':
    app.run(debug=True)