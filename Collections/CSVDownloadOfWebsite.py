# -*- coding: utf-8 -*-

import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import io
import requests
from io import StringIO
import csv

class CSVDownloadOfWebsite():

    def __init__(self, url):
        self.url = url

    def download(self):

        output = []

        try:
            http = urllib3.PoolManager()
            request = http.request("GET", self.url)

            if request.status == 200:
                data = "".join(map(chr, request.data))
                #print(data)
                data = data.split('\n')
                for row in data:
                    output.append(row)
                    #print(row)  # or print(row.split(','))
            else:
                exit("Der Requeststatus hat den Status" + str(request.status) + " und wurde abgebrochen!")

            return output

        except Exception as e:
            print(e)




    def download2(self):

        try:
            http = urllib3.PoolManager()
            request = http.request('GET', self.url)
            if request.status == 200:
                data = request.data
                return data
            else:
                exit("Der Requeststatus hat den Status" + str(request.status) + " und wurde abgebrochen!")

        except Exception as e:
            print(e)
