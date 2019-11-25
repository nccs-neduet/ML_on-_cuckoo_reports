import os
import json
import numpy as np
from dictor import dictor
from pandas.io.json import json_normalize
from sklearn.feature_extraction.text import CountVectorizer

master_list = []


def dict_or_list2(list_or_dict,original_json, column_name = None, previous_key = None, count = 0):
    # print("in function")
    
    if column_name ==  None:
        
        column_name = ""


    if type( list_or_dict ) is dict:
        # print("Dictionary Encountered")
        for key, value in list_or_dict.items():

            

            if column_name == "":
                # print( "Column name is empty" )
                separator = ""
                previous_key = key
            else:
                separator = "."
                # print( "Column name is not empty" )
                # print(column_name )
           
            if previous_key is not None:
                # print( "Column name before removal ", column_name )
                # print("previous key", previous_key)
                column_name = column_name[:column_name.rfind( str( previous_key ) ) + len( str(previous_key)  ) ]
                # print( "Column name after removal ", column_name )
                # column_name = column_name[:column_name.rfind( str( previous_key ) ) - 1]

            column_name = column_name + separator + str( key )
            count = count + 1
            # print(key)
            # print(key, end = ' ')

            if ( ( type( value ) is dict ) or ( type( value ) is list ) ) and bool(value):

                if dictor(original_json, column_name,default="non_existing") == "non_existing":
                    column_name = column_name[column_name.find( str( previous_key ) ) + len( str(previous_key)  ) + 1: ]
                # print(column_name )
                # print( "Count: {}, Previous Key: {}".format( count, previous_key ) )
                
                dict_or_list2( value, original_json, column_name, previous_key=key, count=count )

            else:
                if dictor(original_json, column_name,default="non_existing") == "non_existing":
                    column_name = column_name[column_name.find( str( previous_key ) ) + len( str(previous_key)  ) + 1: ]
                # print(column_name )
                master_list.append( str(column_name) )
                column_name = column_name[:column_name.rfind( str( key ) ) - 1]
                

    elif type( list_or_dict ) is list:
        # print("List Encountered")
        for index, value in enumerate(list_or_dict) :

            if column_name == "":
                separator = ""
                previous_key = index
            else:
                separator = "."

            if previous_key is not None:
                column_name = column_name[:column_name.rfind( str( previous_key ) ) + len( str(previous_key) ) ]
                # column_name = column_name[:column_name.rfind( str( previous_key ) ) - 1]

            column_name = column_name + separator + str( index )
            count = count + 1
            # print( str(index), end = ' ' )

            if ( ( type( value ) is dict ) or ( type( value ) is list ) ) and bool(value):
                # if dictor(original_json, column_name, checknone=True) == None:
                if dictor(original_json, column_name,default="non_existing") == "non_existing":
                    column_name = column_name[column_name.find( str( previous_key ) ) + len( str(previous_key)  ) + 1: ]
                # print(column_name )
                # print( "Count: {}, Previous Key: {}".format( count, previous_key ) )
                
                dict_or_list2( value,original_json, column_name, previous_key=str(index), count=count )

            else:
                # if dictor(original_json, column_name) == None:
                if dictor(original_json, column_name,default="non_existing") == "non_existing":
                    column_name = column_name[column_name.find( str( previous_key ) ) + len( str(previous_key)  ) + 1: ]
                # print(column_name )
                master_list.append( str(column_name) )
                column_name = column_name[:column_name.rfind( str( index ) ) - 1]
                           
path = "./resources/Reports"

for (dirpath, dirnames, filenames) in os.walk(path):
    
    for indivual_file in filenames:
        print("indivual file: ", indivual_file)
        
        if indivual_file.endswith('.json'): 
            
            with open( os.path.join(path,indivual_file), 'r') as json_report_file:
                
                json_report_dict =  json.load(json_report_file)
                
                nested_element = dict_or_list2(json_report_dict,json_report_dict, previous_key="")
       



master_list_unique = set( master_list )
with open( "./resources/cuckoo_attributes.csv", "w" ) as unique_words:

    for item in master_list_unique:
        unique_words.write(item)
        unique_words.write(",\n")


# print( set( master_list ) )
