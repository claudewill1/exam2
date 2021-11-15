from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import user, car, owner


class OwnerList:
    db = "exam_2"
    def __init__(self,data) -> None:
        self.owner_id = data["owner_id"]
        self.car_id = data["car_id"]
        self.user = None

    @classmethod
    def addPurchase(cls,data):
        query = "INSERT INTO purchases (owner_id, car_id) VALUES (%(owner_id)s,%(car_id)s);"
        results = connectToMySQL(cls.db).query_db(query,data)
        
        return results

    