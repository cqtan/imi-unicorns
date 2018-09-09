from flask import Flask
from pymongo import MongoClient


# Setup Flask app
app = Flask(__name__)
app.config.from_object('app.config')

# Setup MongoDB connection
client = MongoClient('localhost', 27017)
db = client['unicorns']

from app import category_controller, image_controller, book_controller, genre_controller, maps_controller, color_controller

# Instantiate controller classes so they can be used in the project
category_controller = category_controller.Category_Controller()
image_controller = image_controller.Image_Controller()
books_controller = book_controller.Book_Controller()
genre_controller = genre_controller.Genre_Controller()
maps_controller = maps_controller.Maps_Controller()
color_controller = color_controller.Color_Controller()

from app import api

if __name__ == '__main__':
    app.run(debug=True)
