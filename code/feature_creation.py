# Import relavent libraries
import json
import pandas as pd
import csv
import os

# features to be located in cuckoo response
required_features = [ "behavior.processes.modules.basename",\
                      "signatures.marks.call.api",\
                      "signatures.marks.ioc",\
                      "network.domains.domain"]


# function to extract instances of a single feature in report
def feature_extraction_sans_loop(json_variable, feature_accessor):

    print( "function started" )

    if feature_accessor:

        indiviual_keyIndex = 0
        indiviual_key = feature_accessor[0]
            
        print( "feature Accessor: ", feature_accessor )
        print( "indiviual key: ", indiviual_key )
        
        if type( json_variable ) is dict:

            print("is a dictionary")

            if not json_variable:

                print( "Dict is empty...." )

                return

            print("\n"*5)
            print("before change json_variable", json_variable )
            print("\n"*5)

            if indiviual_key in json_variable.keys():
                
                print("key Found")
                json_variable =  json_variable[indiviual_key]

            else:
                print( "no key, skipping" )
                return



            print("\n"*5)
            print("json_variable", json_variable )
            print("\n"*5)
            print("feature Accessor", feature_accessor[indiviual_keyIndex+1:] )
            print("\n"*5)

            if not ( ( type( json_variable ) is dict ) or ( type( json_variable ) is list ) ) and bool(json_variable):

                    print("Values")
                    master_list_value.append(json_variable)
            else:

                

                feature_extraction_sans_loop( json_variable, feature_accessor[indiviual_keyIndex+1:] )

        elif type( json_variable ) is list:


            print("is a list")

            if not json_variable:

                print( "List is empty...." )

                return

            print("list starts")
            
            for index, value in enumerate( json_variable ):
                
                print( "printing list value ",value )
                
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
            if ( indiviual_keyIndex == ( len(feature_accessor) - 1) ) :
                print("\n"*5)
                print( "end of line" )
                print( "indiviual_keyIndex ", indiviual_keyIndex )
                print( "feature_accessor len", len(feature_accessor)  )
                print( "feature_accessor", feature_accessor )
                print("json_variable", json_variable )
                print("\n"*5)

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

        else:
            
            print("Value found")
            print(json_variable)

    print( "function ended" )


# Set dataframe , file path and list containers

feature_frame = pd.DataFrame()

path = "./resources/Reports"

# for (dirpath, dirnames, filenames) in os.walk(path):

# for files in os.listdir(path)
#     print( "Filename", filenames )

unique_features = []
unique_features.clear()

master_list_value = []
master_list_value.clear()

# traverse over report folder and apply 
# feature extraction on indivual reports
for filename in os.listdir(path):

    print( "[INFO] {} in process....".format( filename ) )

    if filename.endswith('.json'): 

        unique_features = []
        unique_features.clear()

        master_list_value = []
        master_list_value.clear()

        with open( os.path.join( path, filename ), "r" ) as indiviual_report:

        

            # with open( "./resources/Reports/report.json", 'r' ) as indiviual_report:

            indiviual_report_json =  json.load( indiviual_report )

            for indiviual_required_feature in  required_features:
            
                tryout = indiviual_required_feature.split(".")
                # tryout = required_features[0].split(".")

                print(tryout)

                # feature_extraction( indiviual_report_json, tryout )
                print( "master_list_value before populating: ", master_list_value  )
                feature_extraction_sans_loop( indiviual_report_json, tryout )
                print( "master_list_value after populating: ", master_list_value  )

                # feature_frame["file"] = [filename]
                # feature_frame = feature_frame.append( {"file" :filename } , ignore_index = True )
                # feature_frame.set_index('file', drop=True, inplace=True)
                # feature_frame.loc[filename] = None

                feature_frame.at[filename, "Placeholder"] = 0

                for item in master_list_value:

                    print( "Item: ", item )
                    
                    temp_feature = indiviual_required_feature + "." + item
                    # temp_feature = required_features[0]+ "." + item

                    unique_features.append( temp_feature )

                    # feature_frame[ temp_feature ] = 1
                    feature_frame.at[ filename, temp_feature] = 1
                    # feature_frame = feature_frame.append( {temp_feature :1 } , ignore_index = True )

            print("Unique Features: ", unique_features)

            print( feature_frame.head() )

# save extracted features in a CSV file 
with open("./resources/feature_frame.csv", 'w') as f:
    # df.to_csv(f, header=False)

    feature_frame.to_csv( f )

