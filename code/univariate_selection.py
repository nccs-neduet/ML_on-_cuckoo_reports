import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

import json

data = pd.read_csv("./resources/feature_frame.csv")

X = data.iloc[:,2:]  #independent columns
y = data.iloc[:,1]    #target column i.e malicious or benign

n_important_features = 50

#apply SelectKBest class to extract top 10 best features
bestfeatures = SelectKBest(score_func=chi2, k=n_important_features)
fit = bestfeatures.fit(X,y)
dfscores = pd.DataFrame(fit.scores_)
dfcolumns = pd.DataFrame(X.columns)

#concat two dataframes for better visualization 
featureScores = pd.concat([dfcolumns,dfscores],axis=1)
featureScores.columns = ['Specs','Score']  #naming the dataframe columns

# getting the top n features interms of importance, 50 in this cast
important_features = featureScores.nlargest(n_important_features,'Score')
print(important_features)  #print 10 best features  
print( "Type( featureScores ): ", type( important_features ) )

# converting the important features into json for parsing
important_features_json = important_features.to_json(orient='records')
print("\n\n\n\n", important_features_json)

# save the important features to json file
with open('./resources/features.json', 'w') as json_file:
    
    json_file.write(important_features_json)

