import pandas as pd

from sklearn.model_selection import cross_val_score
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

#create a new KNN model
knn_cv = KNeighborsClassifier(n_neighbors=3)
#train model with cv of 5 
cv_scores = cross_val_score(knn_cv, X, y, cv=5)
#print each cv score (accuracy) and average them
print(cv_scores)
print("cv_scores mean:{}".format(np.mean(cv_scores)))


# Fit the classifier to the data
knn_cv.fit(X_train,y_train)

#show first 5 model predictions on the test data
knn.predict(X_test)[0:5]