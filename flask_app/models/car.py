from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import user
class Car:
    def __init__(self,dbData) -> None:
        self.id = dbData["id"]
        self.model = dbData["model"]
        self.make = dbData["make"]
        self.year = dbData["year"]
        self.description = dbData["description"]
        self.created_at = dbData["created_at"]
        self.updated_at = dbData["updated_at"]
        self.user_id = dbData["user_id"]

    @classmethod
    def createReport(cls,info):
        query = "INSERT INTO cars (model,make,description,price,year,user_id) VALUES (%(model)s,%(make)s,%(description)s,%(price)s,%(year)s,%(user_id)s);"
        data = {
            "model": info["model"],
            "make": info["make"],
            "description": info["description"],
            "price": info["price"],
            "year": info["year"],
            "user_id": info["user_id"]
        }
        new_car_id = connectToMySQL(cls.db).query_db(query,data)
        return new_car_id
    @classmethod
    def getAllCars(cls):
        query = "SELECT * FROM cars AS sr LEFT JOIN users AS u ON u.id WHERE u.id = user_id;"
        results = connectToMySQL(cls.db).query_db(query)
        all_cars = []
        
        for car in results:
            new_car = cls(car)
            userData = { 
                'id': car['user_id'],
                'first_name': car['first_name'],
                'last_name': car['last_name'],
                'email': car['email'],
                'password': car['password'],
                'created_at': car['created_at'],
                'updated_at': car['updated_at']
            }
            userD = user.User(userData)
            print(userD)
            new_car.user = userD
            all_cars.append(new_car)
        return all_cars