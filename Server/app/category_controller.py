from app import db
from bson.json_util import dumps


class Category_Controller:

    def get_features(self):
        features = db.features.find()

        return dumps(features)
