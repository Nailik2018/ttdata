# -*- coding: UTF-8 -*-

from Collections.CSVDownloadOfWebsite import CSVDownloadOfWebsite
from Collections.helpfunctions.DataClean import DataClean
from Collections.Database import Database
from unidecode import unidecode

import json, ast

import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")

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

        #current_club = ("Rio-Star Muttenz",)

        #is_club_in_table_club = db.sqlstatement("SELECT * FROM club WHERE clubname = %s", current_club)

        for male_player in male_players:

            current_club = (male_player['club'],)

            is_current_club_in_table_club = db.sqlstatement("SELECT * FROM club WHERE clubname = %s", current_club)

            #encoded_club = male_player['club'].decode('utf-8')

            c = male_player['club']
            d = c.encode("utf-8")
            u = {u'club': u'' + c}
            e = format(c)

            print(c)
            print(d)
            print(d.decode('utf-8'))
            print(str(ast.literal_eval(json.dumps(u['club']))))
            print(unidecode(c))
            stdout_encoding = sys.stdout.encoding
            print(stdout_encoding)
            stdout_encoding = sys.stdout.encoding or sys.getfilesystemencoding()
            print(stdout_encoding)

            #f = str(c.decode('utf-8'), 'utf-8')
            #print(f)




            print("-" * 100)


            if not is_current_club_in_table_club:

                #c = male_player['club'].encode('utf-8')
                #print(c)

                #print(unichr(241).encode('utf8'))

                current_club = ('Null', male_player['club'])
                #current_club = ('Null', encoded_club)
                insert_statement = """INSERT INTO club (id, clubname) VALUES (%s, %s)"""
                db.insertstatement3(insert_statement, current_club)

            else:

                #club_id =
                print("else")

        exit()
