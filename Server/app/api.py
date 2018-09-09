""" This class is responsilbe for handeling all rest-calls and sending the required files to the Browser """
import os
import json

from urllib.parse import unquote
from flask import jsonify, send_from_directory
from app import app
from app import books_controller, category_controller, image_controller, genre_controller, maps_controller, color_controller

BASE_URL = os.path.abspath(os.path.dirname(__file__))
CLIENT_APP_FOLDER = os.path.join(BASE_URL, "../../WebApp")


# --------- Rest Calls


@app.route('/api/get-features', methods=['GET'])
def categories():
    return category_controller.get_features()


@app.route('/api/category/<string:feature>/images', methods=['GET'])
def feature_images(feature):
    return image_controller.get_images_by_feature(feature)


@app.route('/api/category/<string:feature>/first-image', methods=['GET'])
def first_image_of_feature(feature):
    return image_controller.get_one_image_by_feature(feature)


@app.route('/api/books/category/<string:cluster>/<int:from_date>/<int:to_date>', methods=['GET'])
def get_ppns_by_cluster_in_range(cluster, from_date, to_date):
    return books_controller.get_ppns_by_cluster_in_range(cluster, from_date, to_date)


@app.route('/api/books/category/<string:cluster>/range', methods=['GET'])
def get_cluster_range(cluster):
    return books_controller.get_range_of_category(cluster)


@app.route('/api/get-subjects', methods=['GET'])
def genres():
    return genre_controller.get_genres()


@app.route('/api/genre/<string:subject>/images', methods=['GET'])
def subject_image(subject):
    return image_controller.get_images_by_subject(unquote(subject))


@app.route('/api/genre/<string:subject>/first-image', methods=['GET'])
def first_image_of_subject(subject):
    return image_controller.get_one_image_by_subject(unquote(subject))


@app.route('/api/books/genre/<string:subject>/range', methods=['GET'])
def get_subject_range(subject):
    return books_controller.get_range_of_subject(subject)


@app.route('/api/books/genre/<string:subject>/<int:from_date>/<int:to_date>', methods=['GET'])
def get_ppns_subject_in_range(subject, from_date, to_date):
    return books_controller.get_ppns_by_subject_in_range(subject, from_date, to_date)


@app.route('/api/get-colors', methods=['GET'])
def get_colors():
    return color_controller.get_colors()


@app.route('/api/color/<string:color>/images', methods=['GET'])
def color_images(color):
    return image_controller.get_images_by_color(color)


@app.route('/api/books/color/<string:color>/range', methods=['GET'])
def get_color_range(color):
    return books_controller.get_range_of_color(color)


@app.route('/api/books/color/<string:color>/<int:from_date>/<int:to_date>', methods=['GET'])
def get_ppns_color_in_range(color, from_date, to_date):
    return books_controller.get_ppns_by_color_in_range(color, from_date, to_date)


@app.route('/api/book/identifier/<string:identifier>/information', methods=['GET'])
def get_information_for_identifier(identifier):
    return books_controller.get_information_for_identifier(identifier)


@app.route('/api/booksInformation', methods=['GET'])
def books():
    return books_controller.get_books()


@app.route('/api/maps-long-lat', methods=['GET'])
def latLong():
    return maps_controller.get_LongLat_informations()


@app.route('/api/min-max', methods=['GET'])
def getMinMax():
    return books_controller.get_minMax()


@app.route('/api/image/<string:object_id>', methods=['GET'])
def get_image(object_id):
    return image_controller.get_image(object_id)


# --------- File app


# Catch All urls, enabling copy-paste url
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')  # Catch All urls, enabling copy-paste url
def home(path):
    return send_from_directory(CLIENT_APP_FOLDER, 'index.html')


@app.route('/client-app/<path:filename>')
def client_app_folder(filename):
    return send_from_directory(CLIENT_APP_FOLDER, filename)


@app.route('/dist/ChasingUnicornsAndVampires/<path:filename>')
def client_app_app_folder(filename):
    return send_from_directory(os.path.join(CLIENT_APP_FOLDER, "dist/ChasingUnicornsAndVampires"), filename)
