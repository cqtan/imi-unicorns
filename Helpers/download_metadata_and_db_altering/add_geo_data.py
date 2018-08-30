import pymongo
from pymongo import MongoClient
import urllib.request
from urllib.parse import urlparse
import json
from geopy.geocoders import Nominatim
import pickle
import time


# set connection to mongodb
client = MongoClient()
# choose db
db = client.unicorn
# choose table
books = db.books
# all entries
book_entries = books.find()[]

broken_ppns = []

geolocator = Nominatim(timeout=5)

osmNominatimURL="http://nominatim.openstreetmap.org/search?format=json&namedetails=1&q="
#latLng = dict()

cache = dict()
count = 0
length = book_entries.count()

for book in book_entries:
    time.sleep(1) # make sure not to send too many requests too quickly to osm
    print(str(count) + " of " + str(length))
    count += 1
    
    if type(book['coverage']) is str:
        location = book['coverage']
    elif type(book['coverage']) is float or not book['coverage']:
        location = 'Unbekannt'
    else:
        location = book['coverage'][0]
        book['coverage'] = location
    #print(location)
    
    if not location in cache.keys():
        geo = geolocator.geocode(location)
        if geo:
            #print(geo.longitude, geo.latitude)
            cache[location] = [geo.longitude, geo.latitude]
            book['longitude'] = geo.longitude
            book['latitude'] = geo.latitude
        else:
            broken_ppns.append(book['identifier'])
            cache[location] = [None, None]
            book['longitude'] = None
            book['latitude'] = None
    else:
        #print("taking from cache")
        book['longitude'] = cache[location][0]
        book['latitude'] = cache[location][1]
    
    books.update_one({'_id': book['_id']}, {"$set": book}, upsert=False)
    

print("PPNS that didn't work:")
print(broken_ppns)

pickle.dump( broken_ppns, open( "broken_ppns_geo.pickle", "wb" ) )

#     locURL=osmNominatimURL+urllib.parse.quote(location).replace(" ","+")
#     try:
#         response = urllib.request.urlopen(locURL)
#         str_response = response#.read().decode('utf-8')
#         data = json.load(str_response)
#         latLng[location]=dict()
#         if len(data)>0:
#             print(data[0])
#             latLng[location][u'lat']=data[0]["lat"]
#             latLng[location][u'lng']=data[0]["lon"]
#             #print location
#             names[location]=dict()
#             if len(data[0]['namedetails'])>0:
#                 for k,v in data[0]['namedetails'].items():
#                     names[location][k]=v
#             else:
#                 names[location][u'name']=location
#                 print("No namedetails for "+location)
#             print(names[location])
#         else:
#             latLng[location]=None
#     except IOError:
#         printLog("\tCould not open: "+locURL)
#         pickleCompress('./picklez/save_names.picklez',names)
#         pickleCompress('./picklez/save_latLng.picklez',latLng)
#         time.sleep(1) # see http://wiki.openstreetmap.org/wiki/Nominatim_usage_policy
# printLog("Done.")

