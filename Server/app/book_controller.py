import math
from app import db
from bson.json_util import dumps


class Book_Controller:
    def get_range_of_category(self, category):
        minmax = {}
        min = db.books.find({"features": category, "date": {"$ne": math.nan}}, {
                            "date": 1}).sort("date", 1).limit(1)
        max = db.books.find({"features": category, "date": {"$ne": math.nan}}, {
                            "date": 1}).sort("date", -1).limit(1)

        for i, j in zip(min, max):
            minDate = int(i["date"])
            maxDate = int(j["date"])

            min = minDate
            max = maxDate

            minmax = {
                "min": min,
                "max": max
            }

        return dumps(minmax)

    def get_ppns_by_cluster_in_range(self, feature, from_date, to_date):
        from_date = str(from_date)
        to_date = str(to_date)
        ppns = db.books.find({"features": feature, "date": {"$gte": from_date, "$lte": to_date}}, {"identifier": 1})

        return dumps(ppns)

    def get_range_of_subject(self, subject):
        minmax = {}
        min = db.books.find({"subject": subject, "date": {"$ne": math.nan}}, {
                            "date": 1}).sort("date", 1).limit(1)
        max = db.books.find({"subject": subject, "date": {"$ne": math.nan}}, {
                            "date": 1}).sort("date", -1).limit(1)

        for i, j in zip(min, max):
            minDate = int(i["date"])
            maxDate = int(j["date"])

            min = minDate
            max = maxDate

            minmax = {
                "min": min,
                "max": max
            }

        return dumps(minmax)

    def get_ppns_by_subject_in_range(self, subject, from_date, to_date):
        from_date = str(from_date)
        to_date = str(to_date)
        ppns = db.books.find({"subject": subject, "date": {"$gte": from_date, "$lte": to_date}}, {"identifier": 1})

        return dumps(ppns)

    def get_range_of_color(self, color):
        minmax = {}
        min = db.books.find({"colors": color, "date": {"$ne": math.nan}}, {
                            "date": 1}).sort("date", 1).limit(1)
        max = db.books.find({"colors": color, "date": {"$ne": math.nan}}, {
                            "date": 1}).sort("date", -1).limit(1)

        for i, j in zip(min, max):
            minDate = int(i["date"])
            maxDate = int(j["date"])

            min = minDate
            max = maxDate

            minmax = {
                "min": min,
                "max": max
            }

        return dumps(minmax)

    def get_ppns_by_color_in_range(self, subject, from_date, to_date):
        from_date = str(from_date)
        to_date = str(to_date)
        ppns = db.books.find({"colors": subject, "date": {"$gte": from_date, "$lte": to_date}}, {"identifier": 1})

        return dumps(ppns)

    def get_information_for_identifier(self, identifier):
        book = db.books.find_one({'identifier': identifier}, {'title': 1, 'date': 1, 'creator': 1, 'publisher': 1, 'longitude':1, 'latitude':1})
        return dumps(book)

    def get_books(self):
        data = []

        for item in db.books.find({'latitude': {'$ne': None},'longitude': {'$ne': None},'date': {'$ne': math.nan}, 'creator': {'$ne': math.nan}}, {'creator': 1, 'title': 1, 'latitude': 1, 'longitude': 1, 'identifier': 1,'date':1}):
            entry = dict()
            entry['geoData'] = [item['latitude'], item['longitude']]
            entry['title'] = item['title']
            entry['date'] = item['date']

            if len(item['creator']) > 0:
                entry['creator'] = str(item['creator'][0])
            else:
                entry['creator'] = ''
            entry['identifier'] = item['identifier']
            
            data.append(entry)

        return dumps(data)

    def get_minMax(self):
        minmax = {}
        min = db.books.find({'latitude': {'$ne': None},'longitude': {'$ne': None},'date': {'$ne': math.nan}, 'creator': {'$ne': math.nan}}, {'date':1}).sort("date", 1).limit(1)
        max = db.books.find({'latitude': {'$ne': None},'longitude': {'$ne': None},'date': {'$ne': math.nan}, 'creator': {'$ne': math.nan}}, {'date':1}).sort("date", -1).limit(1)

        for i, j in zip(min, max):
            minDate = int(i["date"])
            maxDate = int(j["date"])

            min = minDate
            max = maxDate

            minmax = {
                "min": min,
                "max": max
            }
        return dumps(minmax)
