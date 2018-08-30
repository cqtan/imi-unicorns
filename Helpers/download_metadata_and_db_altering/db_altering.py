import pymongo
from pymongo import MongoClient
import json
import pickle
import time
import re
import csv
import numpy as np
import ast
import h5py

# This script contains different snippets for altering the db or adding new components

# set connection to mongodb
client = MongoClient()
# choose db
db = client.unicorn
# choose table
books = db.books
images = db.images
colors = db.colors
# all entries

book_entries = books.find()


rows = pickle.load(open('PATH/TO/images_names_reduced.pkl', 'rb'))
ids = pickle.load(open('PATH/TO/image_ids.pkl', 'rb'))

with h5py.File('PATH/TO/similarities.hdf5', 'r') as f:
   similarities = np.array(f.get('similarities')).astype(str)


# for block in similarities[5:2]:
#         regx = re.compile(image[1] + "$")
#         entry = images.find_one({"ppn": image[0], "path": regx})
#         entry['siblings'] = block[idx]
#         print(image[1], entry['siblings'])
# print(len(rows), len(similarities))

# update images with similarities
# count = 0
# for idx, row in enumerate(rows):
#     print(idx)
#     regx = re.compile(row[1] + "$")
#     # print(row)
#     entry = images.find_one({"ppn": row[0], "path": regx})
#     delimiter = row.find('_')
#     end = len(row)
#     ppn = row[0:delimiter]
#     path = row[(delimiter+1):end]
#     regx = re.compile(path + "$")
#     entry = images.find_one({"ppn": ppn, "path": regx})
#     if entry:
#         block = similarities[idx]
#         # print(block)
#         image_arr = []
#         for image in block:
#             reg = re.compile(image[1] + "$")
#             im = images.find_one({"ppn": "PPN" + image[0], "path": reg})
#             if im:
#                 image_arr.append(im["_id"])
#         entry['siblings'] = image_arr
#         # print(image_arr)
#         images.update_one({'_id': entry['_id']}, {"$set": entry}, upsert=False)
#         count += 1

# print("Updated: " +str(count))

# Update images with colors
# for i, row in enumerate(rows):
#     print("Updating: " + str(i))
#     colors = []
#     # if i == len(rows)-10:
#     # print(row[0], row[1])
#     regx = re.compile(row[1] + "$")
#     entry = images.find_one({"ppn": row[0], "path": regx})
#     # entry = images.find({"ppn": row[0]})
#     if entry:
#         hex_codes = row[3]
#         for code in hex_codes:
#             #print(code)
#             colors.append(code)
#         entry['colors'] = colors
#         images.update_one({'_id': entry['_id']}, {"$set": entry}, upsert=False)
#         count +=1 

# print("Images updated: " + str(count))

# image_entries = images.find()

# col_arr = []
# count = 0
# for image in image_entries:
#     print("Row: " + str(count) + " " + image['ppn'])
#     count += 1
#     cols = image['colors']
#     for c in cols:
#         if c not in col_arr:
#             col_arr.append(c)
#             colors.insert_one({'name': c})



# Replace XX with 00 on Year-Dates for prettification
# x_pattern = re.compile("..XX")

# for book in book_entries:
#     #book['identifier']
#     if type(book['date']) is str and x_pattern.match(book['date']):
#         book['date'] = book['date'].replace('XX', '00')
#     if "\n" in book['identifier']:
#         #print(book['identifier'])
#         book['identifier'] = book['identifier'].replace("\n", '')
#     if "PPNPPN" in book['identifier']:
#         book['identifier'] = book['identifier'].replace('PPNPPN', 'PPN')
#         print(book['identifier'])
        

#     books.update_one({'_id': book['_id']}, {"$set": book}, upsert=False)
