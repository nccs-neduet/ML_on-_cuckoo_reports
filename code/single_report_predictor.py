import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

import pickle
import time
import os
import json
import dictor


cuckoo_report_filename = './resources/Reports/benign_report.json'

# Loading the single json report for 
# important feature extraction and prediction
with open( cuckoo_report_filename, "r" ) as indiviual_report:

    indiviual_report_json =  json.load( indiviual_report )

important_feature_filename = './resources/features.json'

# Loading the important features from json file
with open( important_feature_filename, 'r' ) as feature_json:
    
    important_features = json.load( feature_json )

trained_model_filename = './resources/model/cuckoo_model_knn_03122019-093907_acc_78.95.sav'

# Loading the trained model from pickle file
with open( trained_model_filename, 'rb' ) as model_pickel:

    # load the model from disk
    trained_model = pickle.load(model_pickel)

# if dictor(original_json, column_name,default="non_existing") == "non_existing":

# print( important_features )

feature_in_report = pd.DataFrame()

for feature in important_features:

    feature_list = feature[ 'Specs' ].split( '.' )

    for key in feature_list:

        if ( type( indiviual_report_json ) is dict ):

        elif ( type( indiviual_report_json ) is dict ):

        elif ( ( type( indiviual_report_json ) is dict ) or ( type( indiviual_report_json ) is list ) ) and bool( indiviual_report_json ):


    # last_separator = feature[ 'Specs' ].rfind('.')
    # print( feature[ 'Specs' ] )
    # feature_key_chain
    # print(feature['Specs'][:last_separator])

    # if dictor(indiviual_report_json, feature['Specs'],default="non_existing") != "non_existing":

    #     print("feature found: ")
    #     print( feature['Specs'] )