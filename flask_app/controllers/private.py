from flask_app import app
from flask import Flask, render_template, redirect, request, session
import re
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.car import Car



@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("dashboard.html", user = User.getSingleUser(data), all_cars = Car.getAllCars())


@app.route("/add/<int:id>")
def addCar(id):
    user_id = session["user_id"]
    userById = User.getSingleUser(id)

    return render_template("add.html", user = userById)

@app.route("/createCar/new",methods=["POST"])
def createCar():
    user_id = session["user_id"]
    
    if not Car.validateCar(request.form):
        redirect(f"/add/{user_id}")
    data = {
        "model": request.form["model"],
        "make": request.form["make"],
        "description": request.form["description"],
        "price": request.form["price"],
        "year": request.form["year"],
        "user_id": session["user_id"]
    }
    print(data)
    
        
    Car.createCar(data)
    return redirect("/dashboard")

@app.route("/edit/<int:id>")
def editSighting(id):
    context = {
        "user": User.getSingleUser(session["user_id"]),
        "car": Car.getOneCarById(id)
    }
    return render_template("edit.html",**context)

@app.route("/show/<int:car_id>")
def show(car_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': car_id
    }
    
    return render_template("show.html",car = Car.getOneWithUser(data), user = User.getAllUsers())

@app.route("/purchase/<int:car_id>")
def purchase(car_id):
    Car.deleteCar(car_id)
    return redirect("/dashboard")

@app.route("/car/<int:id>/update",methods=["POST"])
def updateSighting(id):
    if not Car.validateCar(request.form):
        return redirect(f"/edit/{id}")
    data = {
        "id": id,
        "price": request.form["price"],
        "model": request.form["model"],
        "make": request.form["make"],
        "description": request.form["description"],
        "year": request.form["year"],
        "user_id": session["user_id"]
    }
    Car.updateSingleCar(data)
    return redirect("/dashboard")


@app.route("/delete/<int:id>")
def deleteReport(id):
    Car.deleteCar(id)
    return redirect("/dashboard")