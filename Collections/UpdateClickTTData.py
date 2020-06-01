# -*- coding: UTF-8 -*-

from Collections.CSVDownloadOfWebsite import CSVDownloadOfWebsite
from Collections.helpfunctions.DataClean import DataClean
from Collections.Database import Database
from Collections.helpfunctions.tuple_to_list import tuple_to_list

from datetime import datetime

def logik(db, players, gender_id):

    today = datetime.today()
    year = today.year
    month = today.month
    day = today.day

    for player in players:

        # Attribut Werte zuweisung des aktuellen Player aus der CSV Datei
        p_firstname = player['firstname']
        p_lastname = player['lastname']
        p_licence_number = player['licence_number']
        p_new_elo_wert = player['new_elo_wert']
        p_club = player['club']

        # Setzt aus der Datenbank die Club_ID des aktuellen Clubs
        db_club_id = 0

        db_licence_number = None
        db_firstname = None
        db_lastname = None
        db_club_id_2 = None
        db_club = None

        # Überprüfunge aus der Datenbank ob der Spieler der CSV Datei in der Datenbank bereits vorhanden ist
        #db_player = db.sqlstatement("SELECT * FROM player WHERE licenceNr = %s", (p_licence_number,))
        db_player = db.sqlstatement("SELECT * FROM player INNER JOIN club ON club.id = player.clubID  WHERE licenceNr = %s", (p_licence_number,))

        if len(db_player) == 1:

            db_licence_number = db_player[0][0]
            db_firstname = db_player[0][1]
            db_lastname = db_player[0][2]
            db_club_id_2 = db_player[0][3]
            db_club = db_player[0][6]

        # Überprüfunge aus der Datenbank ob der aktuelle Club des Spielr aus der CSV Datei in der Datenbank bereits vorhanden ist
        current_club = (p_club,)
        is_current_club_in_table_club = db.sqlstatement("SELECT id, clubname FROM club WHERE clubname = %s", current_club)

        if not is_current_club_in_table_club:

            # Insert Club in Datenbank
            insert_club_data_of_current_player = ('Null', p_club)
            insert_statement = """INSERT INTO club (id, clubname) VALUES (%s, %s)"""
            db.insertstatement(insert_statement, insert_club_data_of_current_player)

            # Falls kein Club bereits vorhanden war ist nach Insert der Club und Club Id in der Datenbank
            is_current_club_in_table_club = db.sqlstatement("SELECT id, clubname FROM club WHERE clubname = %s",
                                                            current_club)
        # Array von Tuple club_id an Index = 0 0
        db_club_id = is_current_club_in_table_club[0][0]

        # Abhandlung über Spieler welche bereist in der Datenbank vorhanden sind oder nicht.
        # Bei 0 ist der Spieler noch nicht in der Datenbank muss daher zu erst eingefüght werden
        # Bei 1 ist der Spielr bereits in der Datenbank vorhanden muss daher upgedatet werden
        if len(db_player) == 0 and db_club_id > 0:

            insert_current_player = (p_licence_number, p_firstname, p_lastname, db_club_id, gender_id)
            print("len(db_player) == 0 and db_club_id > 0")
            print(insert_current_player)
            insert_statement = ("INSERT INTO player "
                                "(licenceNr, firstname, lastname, clubID, genderID) "
                                "VALUES (%s, %s, %s, %s, %s)")
            db.insertstatementMany(insert_statement, insert_current_player)

        elif len(db_player) == 1:

            print("elif")

            if db_firstname == p_firstname and db_lastname == p_lastname and db_club == p_club:
                print("genau gleich")

            else:

                print("firstname lastname club nicht gleich")
                update_data = (p_firstname, p_lastname, db_club_id, int(p_licence_number))

                update_statement = """UPDATE player SET player.firstname=%s, player.lastname=%s, player.clubID=%s WHERE player.licenceNr = %s""";

                db.updatestatement(update_statement, update_data)

        else:

            print("else")

        print("CSV Datei Attriubte")
        print("Firstname: " + p_firstname)
        print("Lastname: " + p_lastname)
        print("Lizenznummer: " + str(p_licence_number))
        print("Neuer Elo Wert: " + str(p_new_elo_wert))
        print("Club: " + p_club)
        print(player)

        print("Datenbank")
        print("Firstname: " + str(db_firstname))
        print("Lastname: " + str(db_lastname))
        print("Lizenznummer: " + str(db_licence_number))
        print("Club_ID: " + str(db_club_id_2))
        print("-" * 100)

class UpdateClickTTData():

    def __init__(self, male_url, female_url):
        self.male_url = male_url
        self.female_url = female_url

    def update(self):
        male_csv = CSVDownloadOfWebsite(self.male_url)
        female_csv = CSVDownloadOfWebsite(self.female_url)
        row_male_data = male_csv.download()
        row_female_data = female_csv.download()

        male_players = DataClean().cleanDataToArray(row_male_data)
        female_players = DataClean().cleanDataToArray(row_female_data)

        total_males = int(len(row_male_data)) - 1
        total_females = int(len(row_female_data)) - 1

        print(male_players)
        print(female_players)

        db = Database()
        db.connection()

        male_id = 1
        female_id = 2

        logik(db, male_players, male_id)
        #logik(db, female_players, female_id)



        exit("Hallo")










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
                        #update_statement = "UPDATE player SET clubID = %s WHERE licenceNr = %s, (licence_number,)"
                        #db.sqlstatement(update_statement, club_id)
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


    def update2(self):
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