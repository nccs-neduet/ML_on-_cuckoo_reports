import pandas as pd

from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

import numpy as np


#read in the data using pandas
df = pd.read_csv("./resources/feature_frame.csv")
#check data has been read in properly
df.head()

#check number of rows and columns in dataset
df.shape

#create a dataframe with all training data except the target column
X = df.drop(columns=["class"])
X = X.drop(X.columns[1])
X = df[df.columns[2:]]
#check that the target variable has been removed
X.head()

#separate target values
y = df["class"].values
#view target values
y[0:5]

#create new a knn model
knn2 = KNeighborsClassifier()
#create a dictionary of all values we want to test for n_neighbors
param_grid = {"n_neighbors": np.arange(1, 25)}
#use gridsearch to test all values for n_neighbors
knn_gscv = GridSearchCV(knn2, param_grid, cv=5)
#fit model to data
knn_gscv.fit(X, y)

#check top performing n_neighbors value
knn_gscv.best_params_

#check mean score for the top performing value of n_neighbors
knn_gscv.best_score_