# import relavent libraries
import os
import json
import numpy as np
from dictor import dictor
from pandas.io.json import json_normalize
from sklearn.feature_extraction.text import CountVectorizer

# set an list variable 
# to hold features
master_list = []

# function to parse dictionary or list within json
def dict_or_list2(list_or_dict,original_json, column_name = None, previous_key = None, count = 0):
    
    # if this is the first 
    # call to this function
    if column_name ==  None:
        
        column_name = ""

    # evaluate the variable is a dictionary
    if type( list_or_dict ) is dict:
        
        # print("Dictionary Encountered")
        
        # iterate over the keys in a dictionary
        for key, value in list_or_dict.items():

            
            # if colum name is empty 
            if column_name == "":
                
                separator = ""
                previous_key = key

            else:
                
                separator = "."

            # if previous key is already set    
            if previous_key is not None:
                # print( "Column name before removal ", column_name )
                # print("previous key", previous_key)
                column_name = column_name[:column_name.rfind( str( previous_key ) ) + len( str(previous_key)  ) ]
                # print( "Column name after removal ", column_name )
                # column_name = column_name[:column_name.rfind( str( previous_key ) ) - 1]

            # construct nested features with key concatenation
            column_name = column_name + separator + str( key )
            count = count + 1
            # print(key)
            # print(key, end = ' ')

            # if value is encountered instead of a list or dictionary,
            #  indicating one complete nested feature
            if ( ( type( value ) is dict ) or ( type( value ) is list ) ) and bool(value):

                # using dictor library to access json data using the newly constructed nested feature 
                if dictor(original_json, column_name,default="non_existing") == "non_existing":
                    column_name = column_name[column_name.find( str( previous_key ) ) + len( str(previous_key)  ) + 1: ]
                # print(column_name )
                # print( "Count: {}, Previous Key: {}".format( count, previous_key ) )
                
                dict_or_list2( value, original_json, column_name, previous_key=key, count=count )

            else:
                
                # using dictor library to access json data using the newly constructed nested feature 
                if dictor(original_json, column_name,default="non_existing") == "non_existing":
                    column_name = column_name[column_name.find( str( previous_key ) ) + len( str(previous_key)  ) + 1: ]
                # print(column_name )
                master_list.append( str(column_name) )
                column_name = column_name[:column_name.rfind( str( key ) ) - 1]
                
    # evaluate the variable is a list
    elif type( list_or_dict ) is list:
        
        # iterate over the dictionary
        for index, value in enumerate(list_or_dict) :

            # set different separator 
            # if column is empty
            if column_name == "":
                separator = ""
                previous_key = index
            else:
                separator = "."

            # if previous key is already set
            if previous_key is not None:
                column_name = column_name[:column_name.rfind( str( previous_key ) ) + len( str(previous_key) ) ]
                # column_name = column_name[:column_name.rfind( str( previous_key ) ) - 1]

            # construct nested features with key concatenation
            column_name = column_name + separator + str( index )
            count = count + 1
            # print( str(index), end = ' ' )

            # if value is encountered instead of a list or dictionary,
            #  indicating one complete nested feature
            if ( ( type( value ) is dict ) or ( type( value ) is list ) ) and bool(value):
                
                # using dictor library to access json data using the newly constructed nested feature 
                if dictor(original_json, column_name,default="non_existing") == "non_existing":
                    
                    column_name = column_name[column_name.find( str( previous_key ) ) + len( str(previous_key)  ) + 1: ]
                # print(column_name )
                # print( "Count: {}, Previous Key: {}".format( count, previous_key ) )
                
                dict_or_list2( value,original_json, column_name, previous_key=str(index), count=count )

            else:
                
                # using dictor library to access json data using the newly constructed nested feature 
                if dictor(original_json, column_name,default="non_existing") == "non_existing":
                   
                    column_name = column_name[column_name.find( str( previous_key ) ) + len( str(previous_key)  ) + 1: ]
                # print(column_name )
                master_list.append( str(column_name) )
                column_name = column_name[:column_name.rfind( str( index ) ) - 1]

# set the folder path
path = "./resources/Reports"

# iterate over files 
for indivual_file in os.listdir(path):
    print("indivual file: ", indivual_file)
    
    # work on json files only
    if indivual_file.endswith('.json'): 
        
        # open indiviual report
        with open( os.path.join(path,indivual_file), 'r') as json_report_file:
            
            # load json file in variable
            json_report_dict =  json.load(json_report_file)
            
            # send the json variable to function for nested features extraction
            nested_element = dict_or_list2(json_report_dict,json_report_dict, previous_key="")
    


# use python set type casting to get rid of duplicate
master_list_unique = set( master_list )

# write to CSV file to store nested features
with open( "./resources/cuckoo_attributes.csv", "w" ) as unique_words:

    for item in master_list_unique:
        unique_words.write(item)
        unique_words.write(",\n")


# print( set( master_list ) )
