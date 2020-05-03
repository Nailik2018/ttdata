# -*- coding: UTF-8 -*-

import mysql.connector
import datetime
from configparser import ConfigParser
import ast
from Collections.helpfunctions.tuple_to_list import tuple_to_list

class Database():

    def __init__(self):
        mysql = ''

    def connection(self):

        db_config = ConfigParser()
        db_config.read("configurations/database.ini")

        user = ast.literal_eval(db_config.get("DATABASE", "dbuser"))
        db = ast.literal_eval(db_config.get("DATABASE", "db"))
        password = ast.literal_eval(db_config.get("DATABASE", "password"))

        db = db.split("=")

        localhost = db[1].split(";")
        db = db[2]
        localhost = localhost[0]

        self.mysql = mysql.connector.connect(
            host=localhost,
            user=user,
            passwd=password,
            database=db
        )

    def sqlstatement(self, statement, values):

        cursor = self.mysql.cursor()
        cursor.execute(statement, values)
        result = cursor.fetchall()
        #result = tuple_to_list(result)

        return result

    def sqlstatement2(self, statement):

        cursor = self.mysql.cursor()
        cursor.execute(statement)
        result = cursor.fetchall()
        #result = tuple_to_list(result)

        return result

    def insertstatement(self, statement):

        cursor = self.mysql.cursor(prepared=True)
        cursor.execute(statement)
        self.mysql.commit()

    def insertstatement2(self, statement, vals):

        cursor = self.mysql.cursor(prepared=True)
        insert_tuple = vals
        cursor.execute(statement, insert_tuple)
        self.mysql.commit()

    def insertstatement3(self, statement, input):

        cursor = self.mysql.cursor(prepared=True,)
        cursor.execute(statement, input)
        self.mysql.commit()
