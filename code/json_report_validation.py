""" This script allows to check if json files within a folder are valid.
    If the files are corrupted they will be marked with the extension ".corrupt" 
                                                                               """
import os
import json


# set path to the folder containing json reports
path = "/home/zunair/Downloads/reports_benign/"

# loop over all the files with the directory
for filename in os.listdir(path):

    print( "[INFO] Testing {} ....".format( filename ) )
    
    # Only parse json files
    if filename.endswith('.json'):
        
        # try statement to catch 
        # exception and continue execution
        try:
                
            # open file in read mode
            with open( os.path.join( path, filename ), "r" ) as indiviual_report:

                # load the json variable
                indiviual_report_json =  json.load( indiviual_report )


        except Exception as e:

            print( "Exception raised: \n" )
            print(e)

            # renaming corrupt file
            os.rename( os.path.join( path, filename ), os.path.join( path, filename + ".corrupt" ) )
