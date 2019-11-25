import csv

path_feature_file_csv = "./resources/cuckoo_attributes.csv"

temp_csv = []

with open(path_feature_file_csv) as feature_file_csv:
    
    features = csv.reader( feature_file_csv, delimiter=',' )

    for index_r, row in enumerate(features):
        print( "row: {} and Value: {}" .format( index_r, row[0] ) )

        temp_row = ""
        
        split_feature = row[0].split('.')

        for index_w, word in enumerate( split_feature ) :
            
            if not word.isdigit():
                
                temp_row = temp_row + word 
                
                if index_w != len( split_feature ) - 1:
                    temp_row = temp_row + "."
            
        print( "new row: {}" .format( temp_row ) )

        temp_csv.append( temp_row )

    unique_features = list( set( temp_csv ) )

    with open("./resources/unique_features.csv", 'w') as unique_feature_file_csv:

        wr = csv.writer(unique_feature_file_csv, delimiter='\n')
        wr.writerow(unique_features)