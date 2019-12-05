import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

import pickle
import time
import os
import json
import dictor

from fuzzywuzzy import fuzz

# Flatten the json report to simple dictionary
def flatten_json(y):

    out = {}

    # internal function to unfold nested json
    def flatten(x, name=''):

        if type(x) is dict:

            for a in x:

                flatten(x[a], name + a + '*')

        elif type(x) is list:

            i = 0

            for a in x:

                flatten(a, name + str(i) + '*')
                i += 1

        # this condition indicates that 
        # we are at the end of nested chain
        else:
            out[name[:-1]] = x

    flatten(y)

    return out

# convert flattened json dictionary to a list 
# after concatenating key-value pair
def dictionary_to_list(flat_json):

    json_list = []

    # looping over each entry and appending it to a 
    # list after concatenating key and value
    for key, value in flat_json.items():

        json_list.append(str(key) + '*' + str(value))

    return json_list

# remove numbers from list and get unique features
def number_remover(json_list):

    temp_csv = []

    # loop over all the nested features
    for index_r, row in enumerate(json_list):
        # print("row: {} and Value: {}" .format(index_r, row))
        # print( f"row: {index_r} and Value: {row}")

        temp_row = ""

        # split the feature from '.'
        split_feature = row.split('*')
        
        # loop over the separated feature and append
        # to temporary variable, if it is not a digit
        for index_w, word in enumerate(split_feature):
            
            if not word.isdigit():

                temp_row = temp_row + word

                if index_w != len(split_feature) - 1:
                    temp_row = temp_row + "."

        # print("new row: {}" .format(temp_row))

        temp_csv.append(temp_row)

    temp_csv = list(set(temp_csv))

    return temp_csv


trained_feature_filename = './resources/feature_frame.csv'
trained_feature_frame = pd.DataFrame()

# Loading the trained feature CSV for
# only feature extracted and its order
# removing any previous data
with open(trained_feature_filename, "r") as trained_feature_csv:

    trained_feature_frame = pd.read_csv(trained_feature_csv)

    trained_feature_frame = trained_feature_frame.iloc[0:0]

    # print( "Trained Feature CSV Columns: {}".format( trained_feature_frame ) )


cuckoo_report_filename = './resources/Reports/benign_report8.json'

# Loading the single json report for
# important feature extraction and prediction
with open(cuckoo_report_filename, "r", encoding="utf-8" ) as indiviual_report:

    indiviual_report_json = json.load(indiviual_report)

important_feature_filename = './resources/features.json'

# Loading the important features from json file
with open(important_feature_filename, 'r') as feature_json:

    important_features = json.load(feature_json)

trained_model_filename = './resources/model/cuckoo_model_knn_03122019-093907_acc_78.95.sav'

# Loading the trained model from pickle file
with open(trained_model_filename, 'rb') as model_pickel:

    # load the model from disk
    trained_model = pickle.load(model_pickel)

flat_json = flatten_json(indiviual_report_json)

list_json = dictionary_to_list(flat_json)

list_json_sans_number = number_remover(list_json)

feature_in_report = pd.DataFrame()

for feature in important_features:

    highest_ratio = 0

    for item in list_json_sans_number:

        # Ratio = fuzz.ratio(item.lower(),feature['Specs'].lower())
        Ratio = fuzz.partial_ratio(item.lower(), feature['Specs'].lower())

        if Ratio > highest_ratio:

            highest_ratio = Ratio

        if Ratio >= 95:

            # print("feature: {},Item:{} and Ratio:{}".format(feature, item, Ratio ) )

            trained_feature_frame.at["test", feature['Specs']] = 1

trained_feature_frame = trained_feature_frame.fillna(0)
trained_feature_frame.head()

trained_feature_frame = trained_feature_frame[trained_feature_frame.columns[2:]]

prediction_result = trained_model.predict(trained_feature_frame)

print(f"Prediciton result: {prediction_result}")

with open("./resources/test_feature_frame.csv", 'w') as f:

    trained_feature_frame.to_csv(f)


