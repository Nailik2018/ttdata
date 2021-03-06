# -*- coding: utf-8 -*-

from Collections.UpdateClickTTData import UpdateClickTTData

import time

start_time = time.time()

csv_male_download_link = "http://www.click-tt.ch/cgi-bin/WebObjects/nuLigaTTCH.woa/wa/eloRankingsCSV?gender=male"
csv_female_download_link = "http://www.click-tt.ch/cgi-bin/WebObjects/nuLigaTTCH.woa/wa/eloRankingsCSV?gender=female"

click_tt = UpdateClickTTData(csv_male_download_link, csv_female_download_link)
click_tt.update()

end_time = time.time()

duration = end_time - start_time

print("Die Ausführung des Codes dauerte " + str(duration) + " Sekunden")
