import pandas as pd
import csv
import os
from sklearn.ensemble import RandomForestClassifier

path  = "./resources/feature_frame.csv"

# save extracted features in a CSV file 
cuckoo_report_attributes = pd.read_csv(path)

print( cuckoo_report_attributes )



# # Create the model with 100 trees
# model = RandomForestClassifier(n_estimators=100, 
#                                bootstrap = True,
#                                max_features = 'sqrt')
# # Fit on training data
# model.fit(train, train_labels)