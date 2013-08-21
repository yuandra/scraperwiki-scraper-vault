import urllib
import time
import scraperwiki
from geopy import geocoders
g = geocoders.Google(domain='maps.google.co.in')
# Here is an example CSV file
url = "https://inmumzm06.tcs.com/service/home/~/?id=2240&part=2&auth=co&disp=i/mrinal_ap.csv"
f = urllib.urlopen(url)
lines = f.readlines()

import csv
clist = list(csv.reader(lines))
print clist

i=0
sl_no=0
header = clist.pop(0)   
j=2001
    
for row in clist:
    dict(zip(header,row))

for row in clist[8000:10000]:
        time.sleep(2)
    #print dict(zip(header, row))
        i=i+1
        if i>2000:
            break
        else:
            try:
                geocode = g.geocode(row[3]+", "+row[4]+", india",exactly_one=False)
                place,(lat,lon)=geocode[0]
                scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":sl_no,"District":row[4],"Village":row[3],"latitude":lat,"longitude":lon})
            #print geocode[0]
            except:
                lat=0
                lon=0
                scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":sl_no,"District":row[4],"Village":row[3],"latitude":lat,"longitude":lon})
            sl_no+=1
            print(lat,lon)

