# -*- coding: utf-8 -*-

class DataClean():

    def __init__(self):
        pass

    @staticmethod
    def cleanDataToArray(data):

        players = []

        for line in data:
            data_set = line.split(";")

            current_player = {}

            # Titel überspringen
            if data_set[0] == "NACHNAME":
                continue
            else:
                #print(data_set)

                if len(data_set) == 1:
                    continue

                elif len(data_set) >= 9:

                    current_player['lastname'] = data_set[0]
                    current_player['firstname'] = data_set[1]
                    current_player['licence_number'] = data_set[2]
                    current_player['club'] = data_set[3]
                    current_player['new_elo_wert'] = data_set[4]
                    current_player['elo_wert_delta'] = data_set[5]
                    current_player['placement'] = data_set[6]
                    current_player['classment'] = data_set[7]
                    current_player['classment_men'] = data_set[8]

                    players.append(current_player)
                else:
                    print("Dataset zu klein " + str(len(data_set)))

        return players


    @staticmethod
    def cleanDataToArray2(data):

        players = []

        for line in data:
            data_set = line.split(";")

            current_player = {}

            if line == "n\'" or data_set[1] == "VORNAME":
                # print(line)
                continue
            else:
                firstname = ''
                for i in range(0, len(data_set[0])):
                    if i != 0:
                        firstname += data_set[0][i]
                        i += 1
                current_player['firstname'] = firstname
                current_player['lastname'] = data_set[1]
                current_player['licence_number'] = data_set[2]
                current_player['club'] = data_set[3]
                current_player['new_elo_wert'] = data_set[4]
                current_player['elo_wert_delta'] = data_set[5]
                current_player['placement'] = data_set[6]
                current_player['classment'] = data_set[7]
                current_player['classment_men'] = data_set[8]

                players.append(current_player)

        return players
