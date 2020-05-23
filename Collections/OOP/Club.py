# -*- coding: UTF-8 -*-

from Collections.Database import Database

class Club():

    def __init__(self, club):
        self.club = club

    def insertClub(self):

        db = Database()
        db.connection()

        is_current_club_in_table_club = db.sqlstatement("SELECT * FROM club WHERE clubname = %s", self.club)

        if not is_current_club_in_table_club:
            current_club = ('Null', self.club)
            insert_statement = """INSERT INTO club (id, clubname) VALUES (%s, %s)"""
            db.insertstatement(insert_statement, current_club)





