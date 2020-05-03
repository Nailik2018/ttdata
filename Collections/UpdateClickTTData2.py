# -*- coding: utf-8 -*-
from Collections.CSVDownloadOfWebsite import CSVDownloadOfWebsite
from Collections.helpfunctions.DataClean import DataClean
from app4 import ORMCreatAndData

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

        orm = ORMCreatAndData()

        orm.generateGender()

        orm.generateClub("TTC Ostermundigen")
        orm.generateClub("TTC Baar")
        orm.generateClub("TTC Heimberg")

        #for m in male_players:

            #db_clubs = orm.selectClubs()

            #for db_club in db_clubs:
                #print(db_club)

            #orm.generateClub(m['club'])

        #print(total_females)