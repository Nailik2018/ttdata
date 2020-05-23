# -*- coding: UTF-8 -*-

from Collections.CSVDownloadOfWebsite import CSVDownloadOfWebsite
from Collections.helpfunctions.DataClean import DataClean
from Collections.Database import Database
from Collections.helpfunctions.tuple_to_list import tuple_to_list

import json, ast

class UpdateClickTTData():

    def __init__(self, male_url, female_url):
        self.male_url = male_url
        self.female_url = female_url

    def update(self):
        male_csv = CSVDownloadOfWebsite(self.male_url)
        female_csv = CSVDownloadOfWebsite(self.female_url)
        row_male_data = str(male_csv.download())
        row_female_data = str(female_csv.download())

        male_data = row_male_data.split("\\r\\")
        female_data = row_female_data.split("\\r\\")

        male_players = DataClean().cleanDataToArray(male_data)
        female_players = DataClean().cleanDataToArray(female_data)

        total_males = int(len(male_players)) - 1
        total_females = int(len(female_players)) - 1

        db = Database()
        db.connection()

        male_id = 1
        female_id = 2

        for male_player in male_players:

            current_club = (male_player['club'],)
            lastname = male_player['lastname']
            firstname = male_player['firstname']
            licence_number = int(male_player['licence_number'])
            new_elo_wert = male_player['new_elo_wert']

            # Club check ist Club nicht vorhanden wird dieser Club in die Clubtabelle geschrieben
            is_current_club_in_table_club = db.sqlstatement("SELECT id, clubname FROM club WHERE clubname = %s", current_club)

            if not is_current_club_in_table_club:

                current_club = ('Null', male_player['club'])
                insert_statement = """INSERT INTO club (id, clubname) VALUES (%s, %s)"""
                db.insertstatement(insert_statement, current_club)

            if len(is_current_club_in_table_club) >= 1:
                club = list(is_current_club_in_table_club[0])
                club_id = club[0]
                clubname = club[1]

            # Player check ist Player nicht vorhanden wird dieser in die Playertabelle geschrieben
            is_current_player_in_table_player = db.sqlstatement("SELECT * FROM player WHERE licenceNr = %s", (licence_number,))

            if not is_current_player_in_table_player:

                current_player = (licence_number, firstname, lastname, club_id, male_id)

                print("if")
                print(current_player)
                insert_statement = ("INSERT INTO player "
               "(licenceNr, firstname, lastname, clubID, genderID) "
               "VALUES (%s, %s, %s, %s, %s)")
                db.insertstatementMany(insert_statement, current_player)

            else:

                print("else")

                if len(is_current_player_in_table_player[0]) == 5:
                    db_club_of_current_player = is_current_player_in_table_player[0][3]

                    if club_id == db_club_of_current_player:
                        print("same id")
                    else:
                        update_statement = "UPDATE player SET clubID = %s WHERE licenceNr = %s, (licence_number,)"
                        db.sqlstatement(update_statement, club_id)
                        print(str(club_id) + " und " + str(db_club_of_current_player) + " sind nicht identisch")
                    print(db_club_of_current_player)

            print(is_current_player_in_table_player)























        exit()

        for female_player in female_players:

            current_club = (female_player['club'],)

            is_current_club_in_table_club = db.sqlstatement("SELECT * FROM club WHERE clubname = %s", current_club)

            if not is_current_club_in_table_club:

                current_club = ('Null', female_player['club'])
                insert_statement = """INSERT INTO club (id, clubname) VALUES (%s, %s)"""
                db.insertstatement(insert_statement, current_club)
