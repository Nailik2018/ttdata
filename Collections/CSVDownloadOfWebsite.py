# -*- coding: utf-8 -*-

import urllib3

class CSVDownloadOfWebsite():

    def __init__(self, url):
        self.url = url

    def download(self):

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
