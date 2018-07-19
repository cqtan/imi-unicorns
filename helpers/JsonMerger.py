from time import gmtime, strftime, time
import argparse
import logging
import json

# Usage:
# python helpers/JsonMerger.py --json1 test.json --json2 test2.json 
def mergeJson():
    start_time = time()
    output_path = "out"
    file_name = "categories_merged1.json"

    # Configure general logging
    current_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    log_name = 'JsonMerge-LOG_' + current_time + '.log'
    logging.basicConfig(filename=log_name,level=logging.DEBUG)
    logging.info("JSON MERGE SCRIPT")

    ap = argparse.ArgumentParser()
    ap.add_argument("-j1","--json1",type=str, required=True,help="(required) The main json file.")
    ap.add_argument("-j2","--json2",type=str, required=True,help="(required) The json to be merged with.")
    args = vars(ap.parse_args())

    with open(args["json1"]) as json_data:
        json1 = json.load(json_data)

    with open(args["json2"]) as json_data:
        json2 = json.load(json_data)

    category_data1 = json1["category_data"]
    category_data2 = json2["category_data"]
    book_data1 = json1["book_data"]
    book_data2 = json2["book_data"]
    image_data1 = json1["image_data"]
    image_data2 = json2["image_data"]

    # Merge category data
    category_data1.update(category_data2)

    # Merge book data
    for ppn in book_data2:
        # Check if ppn exists already
        if ppn not in book_data1:
            book_data1[ppn] = book_data2[ppn]
        else:
            for feature in book_data2[ppn]:
                # if exists, then append only new features
                if feature not in book_data1[ppn]:
                    book_data1[ppn].append(feature)

    # Merge image data
    unique_image_ref1 = set()
    unique_image_ref2 = set()
    for dict2 in image_data2:
        unique_image_ref2.add(dict2["path"])
        # Check if path exists in image data 1, 
        for dict1 in image_data1:
            unique_image_ref1.add(dict1["path"])
            if dict2["path"] == dict1["path"]:
                # Check features of image data 2 not subset of image data 1, then append to 1
                if not all(f2 in dict1["features"] for f2 in dict2["features"]):
                    new_set = set(dict1["features"])
                    new_set.update(dict2["features"])
                    dict1["features"] = list(new_set)

    # Adding missing image data list values from image data 2
    for val in unique_image_ref2:
        if val not in unique_image_ref1:
            for dict2 in image_data2:
                if dict2["path"] == val:
                    image_data1.append(dict2)

    merged_dict = {
        "category_data": category_data1,
        "book_data": book_data1,
        "image_data": image_data1
    }

    with open(output_path + "/" + file_name, 'w') as json_file:
        json.dump(merged_dict, json_file, indent=4)

    run_duration = (time() - start_time) / 60
    end_msg = "Done! Run Duration:  " + str(run_duration) + " minutes."
    print(end_msg)
    logging.info(end_msg)


if __name__ == '__main__':
    mergeJson()
