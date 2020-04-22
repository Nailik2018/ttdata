# -*- coding: utf-8 -*-
from Collections.CSVDownloadOfWebsite import CSVDownloadOfWebsite
from Collections.helpfunctions.DataClean import DataClean

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

        print(total_males)
        print(total_females)

        print("-" * 100)

        print(male_players)
        print(female_players)