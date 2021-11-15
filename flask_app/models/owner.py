from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import user, car, ownerlist


class Owner:
    db = "exam_2"
    def __init__(self,db_data):
        self.id = db_data["id"]
        self.ownerList = db_data["ownerList"]
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]
        self.user = None
        self.list = []

    @classmethod
    def getAllPurchases(cls):
        query = "SELECT * FROM owner;"
        results = connectToMySQL(cls.db).query_db(query)
        carOwner = []
        for c in results:
            carOwner.append(cls(c))
        return carOwner

    @classmethod
    def getOneCar(cls,data):
        query = "SELECT * FROM owner WHERE id = %(id)s;"
        r = connectToMySQL(cls.db).query_db(query,data)
        return cls(r[0])

    @classmethod
    def getCarOwners(cls,data):
        query = "SELECT * FROM owner WHERE user_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        oList = []
        for o in results:
            oList.append(cls(o))
        return oList

    @classmethod
    def saveOwner(cls,data):
        query = "INSERT INTO owner (ownerList,user_id) VALUES (%(ownerList)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def getOneOwnerWithAUser(cls,id):
        query = "SELECT * FROM owner AS o LEFT JOIN users AS u ON o.user_id = u.id WHERE o.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,id)
        data = {
            "id": results[0]['user_id'], "first_name": results[0]['first_name'], "last_name": results[0]['last_name'], 'email': results[0]['email'],  'password': results[0]['password'], 'created_at': results[0]['created_at'], 'updated_at': results[0]['updated_at']
        }
        print(data)
        car = cls(r[0])
        car.user = user.User.getSingleUser(data)
        return car

    @classmethod
    def getAllCars(cls,data):
        query = "SELECT * FROM owner AS o LEFT JOIN purchases AS p ON owner_id = o.id LEFT JOIN cars AS c ON c.id = car_id LEFT JOIN user AS u ON u.id = o.user_id WHERE o.id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result