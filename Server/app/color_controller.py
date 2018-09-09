from app import db
from bson.json_util import dumps

class Color_Controller:
    def get_colors(self):
        colors = db.colors.find()
        return dumps(colors)
