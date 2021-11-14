from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
NAME_REGEX = re.compile(r'^[a-zA-Z]+[a-zA-Z]+$')
class User:
    db = "exam_2"
    def __init__(self,data) -> None:
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # instance method
    def fullName(self):
        return f"{self.first_name} {self.last_name}"    
        
    @staticmethod
    def validateRegistration(user):
        isValid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) > 0:
            isValid = False
            flash("A user with this email already exists")
        if len(user["password"]) < 8:
            isValid = False
            flash("Password must be at least 6 characters long")
        if len(user["first_name"]) < 2:
            isValid = False
            flash("First name must be at least 2 characters long")
        if len(user["last_name"]) < 2:
            isValid = False
            flash("Last name must be at least 2 characters long")
        if user["password"] != user["confirm"]:
            isValid = False
            flash("Your passwords don't match")
        return isValid

    @classmethod
    def GetUserName(cls,id):
        query = "SELECT first_name, last_name FROM users WHERE id = %(id)s;"
        data = {
            "id": id
        }
        results = connectToMySQL(cls.db).query_db(query,data)
        if not results:
            return False
        return cls(results[0])



    @staticmethod
    def validateLogin(user):
        isValid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(User.db).query_db(query,user)
        if len(result) == 0:
            flash("Email does not exist.")
            isValid = False
        if len(user["email"]) == 0:
            isValid = False
            flash("Email address is required")
        if len(user["password"]) == 0:
            isValid = False
            flash("Password is required")
        return isValid

    @classmethod
    def saveUser(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def getUserByEmail(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def getSingleUser(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
