# Import relavent libraries
import json
import pandas as pd
import csv
import os
import sys
import codecs

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

print( "Start of script" )

blockPrint()

# features to be located in cuckoo response
required_features = [ "behavior.processes.modules.basename",\
                      "signatures.marks.call.api",\
                      "signatures.marks.ioc",\
                      "network.domains.domain"]


# function to extract instances of a single feature in report
def feature_extraction_sans_loop(json_variable, feature_accessor):

    print( "function started" )

    # function will continue only if feature
    # accessor has some value
    if feature_accessor:

        indiviual_keyIndex = 0
        indiviual_key = feature_accessor[0]
            
        print( "feature Accessor: ", feature_accessor )
        print( "indiviual key: ", indiviual_key )
        
        # Evaluate if the variable is a dictionary
        if type( json_variable ) is dict:

            print("is a dictionary")

            # return if the dictionary is empty
            if not json_variable:

                print( "Dict is empty...." )

                return

            print("\n"*5)
            print("before change json_variable", json_variable )
            print("\n"*5)

            # Evaluate if the feature accessor key is
            # present in the dictionary
            if indiviual_key in json_variable.keys():
                
                print("key Found")
                json_variable =  json_variable[indiviual_key]

            else:
                print( "no key, skipping" )
                return



            print("\n"*5)
            print("json_variable", str(json_variable) )
            print("\n"*5)
            print("feature Accessor", feature_accessor[indiviual_keyIndex+1:] )
            print("\n"*5)
            
            # append the data to a list if the variable is a 
            # value instead of being a list or dictionary
            if not ( ( type( json_variable ) is dict ) or ( type( json_variable ) is list ) ) and bool(json_variable):

                    print("Values")
                    master_list_value.append(json_variable)
            else:

                

                feature_extraction_sans_loop( json_variable, feature_accessor[indiviual_keyIndex+1:] )

        # Evaluate if the variable is a list
        elif type( json_variable ) is list:


            print("is a list")

            # return from function if list is empty
            if not json_variable:

                print( "List is empty...." )

                return

            print("list starts")
            
            # loop over the entire list
            for index, value in enumerate( json_variable ):
                
                print( "printing list value ",value )
                
                # if any empty value is encountered in loop,
                # continue to next iteration
                if not value:

                    print( "Nested List is empty...." )

                    continue

                print( "index", index )
                print( "Value", value )

                # json_variable = json_variable[index]

                print("\n"*5)
                print("json_variable", value )
                print("\n"*5)
                print("feature Accessor", feature_accessor[indiviual_keyIndex:] )
                print("\n"*5)

                feature_extraction_sans_loop( value, feature_accessor[indiviual_keyIndex:] )

            print("list ends")

            # check if feature accessor has only one value left
            if ( indiviual_keyIndex == ( len(feature_accessor) - 1) ) :
                print("\n"*5)
                print( "end of line" )
                print( "indiviual_keyIndex ", indiviual_keyIndex )
                print( "feature_accessor len", len(feature_accessor)  )
                print( "feature_accessor", feature_accessor )
                print("json_variable", json_variable )
                print("\n"*5)

            # check if feature accessor has more values
            else:
                print( "else executed " )
                print("\n"*5)
                print( "indiviual_keyIndex ", indiviual_keyIndex )
                print( "feature_accessor len", len(feature_accessor)  )
                print( "feature_accessor", feature_accessor )
                print("json_variable", json_variable )
                print("\n"*5)


                if not json_variable:
                    print("Empty json variable in else....")
                    return
                
                feature_extraction_sans_loop( json_variable, feature_accessor[indiviual_keyIndex+1:] )

        # if the variable is neither 
        # a dictionary or list
        else:
            
            print("Value found")
            print(json_variable)

    print( "function ended" )


# Set dataframe , file path and list variables

feature_frame = pd.DataFrame()

path = "./resources/Reports"

unique_features = []
unique_features.clear()

master_list_value = []
master_list_value.clear()

# traverse over report folder and apply 
# feature extraction on indivual reports
for filename in os.listdir(path):
    enablePrint()
    print( "[INFO] {} in process....".format( filename ) )
    blockPrint()
    # Only parse json files
    if filename.endswith('.json'): 

        unique_features = []
        unique_features.clear()

        master_list_value = []
        master_list_value.clear()

        # open file in read mode
        with open( os.path.join( path, filename ), "r" ) as indiviual_report:

            # load the json variable
            indiviual_report_json =  json.load( indiviual_report )

            # test the file for presence of predefined nested features
            for indiviual_required_feature in  required_features:
            
                tryout = indiviual_required_feature.split(".")
                

                print(tryout)

                # feature_extraction( indiviual_report_json, tryout )
                print( "master_list_value before populating: ", master_list_value  )
                feature_extraction_sans_loop( indiviual_report_json, tryout )
                print( "master_list_value after populating: ", master_list_value  )

                # A class variable for known result
                if "malicious" in filename:
                    feature_frame.at[filename, "class"] = 1
                else:
                    feature_frame.at[filename, "class"] = 0

                # loop over all the fetures extracted
                for item in master_list_value:

                    print( "Item: ", item )
                    
                    temp_feature = indiviual_required_feature + "." + item
                    

                    unique_features.append( temp_feature )

                    
                    feature_frame.at[ filename, temp_feature] = 1
                    

            print("Unique Features: ", unique_features)

            print( feature_frame.head() )

# save extracted features in a CSV file 

with codecs.open("./resources/feature_frame.csv", 'wb', encoding='utf-8', errors='ignore') as f:
# with open("./resources/feature_frame.csv", 'w') as f:
    
    feature_frame.to_csv( f )

    enablePrint()
    
    print( "End of script" )

