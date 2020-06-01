# -*- coding: UTF-8 -*-

from Collections.CSVDownloadOfWebsite import CSVDownloadOfWebsite
from Collections.helpfunctions.DataClean import DataClean
from Collections.Database import Database
from Collections.helpfunctions.tuple_to_list import tuple_to_list

from datetime import datetime

def checkElo(db,):

    check_elo = None


    return check_elo

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
        db_player = db.sqlSelectStatement("SELECT * FROM player INNER JOIN club ON club.id = player.clubID  WHERE licenceNr = %s", (p_licence_number,))

        if len(db_player) == 1:

            db_licence_number = db_player[0][0]
            db_firstname = db_player[0][1]
            db_lastname = db_player[0][2]
            db_club_id_2 = db_player[0][3]
            db_club = db_player[0][6]

        # Überprüfunge aus der Datenbank ob der aktuelle Club des Spielr aus der CSV Datei in der Datenbank bereits vorhanden ist
        current_club = (p_club,)
        is_current_club_in_table_club = db.sqlSelectStatement("SELECT id, clubname FROM club WHERE clubname = %s", current_club)

        if not is_current_club_in_table_club:

            # Insert Club in Datenbank
            insert_club_data_of_current_player = ('Null', p_club)
            insert_statement = """INSERT INTO club (id, clubname) VALUES (%s, %s)"""
            db.sqlInsertStatement(insert_statement, insert_club_data_of_current_player)

            # Falls kein Club bereits vorhanden war ist nach Insert der Club und Club Id in der Datenbank
            is_current_club_in_table_club = db.sqlSelectStatement("SELECT id, clubname FROM club WHERE clubname = %s",
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
            db.sqlInsertStatementMany(insert_statement, insert_current_player)

        elif len(db_player) == 1:

            print("elif")

            if db_firstname == p_firstname and db_lastname == p_lastname and db_club == p_club:
                print("genau gleich")

            else:

                print("firstname lastname club nicht gleich")
                update_data = (p_firstname, p_lastname, db_club_id, int(p_licence_number))

                update_statement = """UPDATE player SET player.firstname=%s, player.lastname=%s, player.clubID=%s WHERE player.licenceNr = %s""";

                db.sqlUpdateStatement(update_statement, update_data)

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
        logik(db, female_players, female_id)

        exit("Hallo")
