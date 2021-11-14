from flask_app import app
from flask import Flask, render_template, redirect, request, session
import re
from flask_bcrypt import Bcrypt
from flask_app.models.user import User



@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("dashboard.html", user = User.getSingleUser(data))

@app.route("/delete/<int:id>")
def deleteReport(id):
    
    return redirect("/dashboard")