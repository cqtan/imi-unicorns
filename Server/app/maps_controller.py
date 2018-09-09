from app import db
from bson.json_util import dumps

class Maps_Controller:

    def get_LongLat_informations(self):
        longLat = []
        for item in db.geoData.find({},{"_id": 0,"latLongCount": 1}):
            longLat.append(item["latLongCount"])

        return dumps(longLat)
  
