import json
import argparse

# Usage: python helpers/JsonRenamer.py -j categories-5.json
ap = argparse.ArgumentParser()
ap.add_argument("-j","--json",type=str, required=True,help="(required) The json file.")
args = vars(ap.parse_args())

with open(args["json"]) as json_data:
    my_json = json.load(json_data)

category_data = my_json["category_data"]
book_data = my_json["book_data"]
image_data = my_json["image_data"]

for my_dict in image_data:
    my_dict["classes"] = my_dict.pop("features")

new_dict = {
    "category_data": category_data,
    "book_data": book_data,
    "image_data": image_data
}

with open("out/renamed.json", "w") as json_file:
    json.dump(new_dict, json_file, indent=4)

print("Done renaming the key to classes!")
