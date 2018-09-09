import math
from pymongo import MongoClient
from categories_list import data

# Setup MongoDB connection
client = MongoClient('localhost', 27017)
db = client['unicorns']

def import_features_to_books(data):
    for key, value in data.items():
        db.books.update({"identifier": key}, {"$set": {"features": value}})

def import_gerne_to_images():
    for image in db.images.find():
        book = db.books.find_one({"identifier": {"$regex": image["ppn"]}})
        db.images.update_many({"_id": image["_id"]}, {"$set": {"subject": book["subject"]}})

def import_colors_to_books():
    images = db.images.find({}, no_cursor_timeout=True)
    for image in images:
        book = db.books.find_one({"identifier": image["ppn"]})
        if "colors" in book:
            book_colors = book["colors"]
            for image_color in image["colors"]:
                if image_color in book_colors:
                    continue
                else:
                    book_colors.append(image_color)
            db.books.update({"identifier": image["ppn"]}, {"$set": {"colors": book["colors"]}})
        else:
            db.books.update({"identifier": image["ppn"]}, {"$set": {"colors": image["colors"]}})
    images.close()


def fix_genres():
    for genre in db.genres.find():
        genre_str = genre["name"]
        update_str = genre_str.replace("/", "")
        db.genres.update({"_id": genre["_id"]}, {"$set": {"name": update_str}})

def fix_subjects():
    for image in db.images.find():
        updated_subjects = []
        for subject in image["subject"]:
            updated_subject = subject.replace("/", "")
            updated_subjects.append(updated_subject)
        db.images.update({"_id": image["_id"]}, {"$set": {"subject": updated_subjects}})

def fix_books():
    for book in db.books.find():
        subject = book["subject"]
        if isinstance(book["subject"], list):
            updated_subjects = []
            for subject in book["subject"]:
                updated_subject = subject.replace("/", "")
                updated_subjects.append(updated_subject)
            db.books.update({"_id": book["_id"]}, {"$set": {"subject": updated_subjects}})
        else:
            updated_subject = subject.replace("/", "")
            db.books.update({"_id": book["_id"]}, {"$set": {"subject": updated_subject}})

def fix_dates():
    for book in db.books.find():
        date = book["date"]

        if isinstance(date, str):
            updated_str = date.replace("X", "0")
            db.books.update({"_id": book["_id"]}, {"$set": {"date": updated_str}})
        

# import_features_to_books(data)
# import_gerne_to_images()
# import_colors_to_books()
# fix_genres()
# fix_subjects()
# fix_books()
fix_dates()
