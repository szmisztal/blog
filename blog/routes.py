from flask import render_template
from blog import app

@app.route('/')
def base():
    return render_template("base.html")
