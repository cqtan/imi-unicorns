from app import db
from bson.json_util import dumps

class Genre_Controller:
    def get_genres(self):
        genres = db.genres.find()

        return dumps(genres)
