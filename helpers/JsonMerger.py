from time import gmtime, strftime
import argparse
import logging
import json


# Usage:
# python JsonMerger.py -json1 categories-5.json -json2 categories-18.json 
def mergeJson():

    output_path = "out"

    # Configure general logging
    current_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    log_name = 'JsonMerge-LOG_' + current_time + '.log'
    logging.basicConfig(filename=log_name,level=logging.DEBUG)
    logging.info("JSON MERGE SCRIPT")

    ap = argparse.ArgumentParser()
    ap.add_argument("-j1","--json1",type=str, required=True,help="(required) The main json file.")
    ap.add_argument("-j2","--json2",type=str, required=True,help="(required) The json to be merged with.")
    args = vars(ap.parse_args())

    with open(args["--json1"]) as json_data:
        json1 = json.load(json_data)

    with open(args["--json2"]) as json_data:
        json2 = json.load(json_data)

    category_data1 = json1[0]
    category_data2 = json2[0]
    book_data1 = json1[1]
    book_data2 = json2[1]
    image_data1 = json1[2]
    image_data2 = json2[2]

    print("Done")


if __name__ == '__main__':
    mergeJson()






