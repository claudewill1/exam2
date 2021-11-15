from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import user
class Car:
    db = "exam_2"
    def __init__(self,dbData) -> None:
        self.id = dbData["id"]
        self.price = dbData["price"]
        self.model = dbData["model"]
        self.make = dbData["make"]
        self.year = dbData["year"]
        self.description = dbData["description"]
        self.created_at = dbData["created_at"]
        self.updated_at = dbData["updated_at"]
        self.user_id = dbData["user_id"]
        self.user = None

    @classmethod
    def createCar(cls,info):
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
        query = "SELECT * FROM cars AS c LEFT JOIN users AS u ON u.id WHERE u.id = user_id;"
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

    @classmethod
    def getOneCarById(cls,id):
        q = "SELECT * FROM cars WHERE id = %(id)s;"
        data = {
            "id": id
        }
        print(id)
        
        res = connectToMySQL(cls.db).query_db(q,data)
        if not res:
            return False
        return cls(res[0])

    @classmethod
    def getOneCar(cls,data):
        query = "SELECT * FROM cars WHERE cars.id = %(id)s;"
        print(id)
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        if not results:
            return False
        return cls(results[0])
    
    @classmethod
    def getOneWithUser(cls,data):
        q = "SELECT * FROM cars AS c LEFT JOIN users AS u ON c.user_id = u.id WHERE c.id = %(id)s;"
        r = connectToMySQL(cls.db).query_db(q,data)
        print(r)
        
        data = {
            "id": r[0]['user_id'], "first_name": r[0]['first_name'], "last_name": r[0]['last_name'], 'email': r[0]['email'],  'password': r[0]['password'], 'created_at': r[0]['created_at'], 'updated_at': r[0]['updated_at']
        }
        print(data)
        car = cls(r[0])
        car.user = user.User.getSingleUser(data)
        return car

    @classmethod
    def purchaseCar(cls,data):
        q = "INSERT INTO purchases (user_id, car_id) VALUES (%(user_id)s,%(car_id)s);"
        return connectToMySQL(cls.db).query_db(q,data)

    
    @classmethod
    def getListOfPurchases(cls,data):
        query = "SELECT * FROM owner AS o LEFT JOIN purchases AS p ON owner_id = o.id LEFT JOIN cars AS c ON c.id = car_id LEFT JOIN user AS u ON u.id = o.user_id WHERE o.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return results

    @classmethod
    def updateSingleCar(cls,info):
        query = "UPDATE cars SET model = %(model)s, make = %(make)s, description = %(description)s, price = %(price)s, year = %(year)s WHERE id = %(id)s;"
        data = {
            "id": info["id"],
            "model": info["model"],
            "make": info["make"],
            "description": info["description"],
            "price": info["price"],
            "year": info["year"]
        }
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def deleteCar(cls,id):
        q = "DELETE FROM cars WHERE id = %(id)s;"
        data = {
            "id": id
        }
        return connectToMySQL(cls.db).query_db(q,data)

    @staticmethod
    def validateCar(data):
        isValid = True
        if len(data["price"]) == 0:
            flash("The car must have a price")
            isValid = False
        if len(data["model"]) < 2:
            flash("Model must be at least two characters long")
            isValid = False
        if len(data["make"]) < 2:
            flash("Make must be at least two characters long")
            isValid = False
        if len(data["year"]) < 4:
            flash("A four digit year is required")
            isValid = False
        if len(data["description"]) == 0:
            flash("description is required")
            isValid = False
        return isValid