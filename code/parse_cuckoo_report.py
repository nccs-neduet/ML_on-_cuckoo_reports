import json
import time
from dictor import dictor
from pandas.io.json import json_normalize

master_list = []

# def dict_or_list(dictionary, key):

#     if type( dictionary[key] ) is dict:
#         return dict
#         print("Dictionary found")

#     elif type( dictionary[key] ) is list:
#         return list
#         print("List found")

#     else:
#         return dictionary[key]
#         print("Value found")


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
            # # if  key == previous_key:
            # #     print("Key not same. Previous key: {} and Key: {}".format( previous_key, key ) )
            # #     print( list_or_dict.keys() )
            # if previous_key not in list_or_dict.keys():
            #     print("Previous key: {} and Key: {}".format( previous_key, key ) )
            #     print( "keys of dictionary: " , list_or_dict.keys() )
            #     column_name = ""

            # print( "\nPrevious Key: {}, Key: {}\n".format( previous_key, key ) )
            # print( "\n", list_or_dict )
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
                print(column_name )
                master_list.append( str(column_name) )
                column_name = column_name[:column_name.rfind( str( key ) ) - 1]
                # print( "Count: {}, Previous Key: {}".format( count, previous_key ) )
                print()
                # return list_or_dict[key]
                print("Value found")
                
                # time.sleep(0.7)

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
                print(column_name )
                master_list.append( str(column_name) )
                column_name = column_name[:column_name.rfind( str( index ) ) - 1]
                # print( "Count: {}, Previous Key: {}".format( count, previous_key ) )
                # return list_or_dict[index]
                print("Value found")
                
                
                # time.sleep(0.7)            



with open("./resources/Reports/report.json", 'r') as json_report_file:
    
    json_report_dict =  json.load(json_report_file)
    # # print( json.dumps(json_report_dict["info"], indent=4) )
    # json_report_dict_normalize = json_normalize( json_report_dict )
    
    # for column in json_report_dict_normalize.columns:
    #     print("\nName of Colums: ", column)    
    # print( json_report_dict_normalize )


    # for key in json_report_dict.keys():

    nested_element = dict_or_list2(json_report_dict,json_report_dict, previous_key="")
    # print(nested_element)
    # print(nested_element, end = '')
    
    # while nested_element == (list or dict):
    #     # print(key)
    #     print(key, end = '')




