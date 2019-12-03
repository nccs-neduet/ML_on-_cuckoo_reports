import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

import pickle
import time


#read in the data using pandas
df = pd.read_csv("./resources/feature_frame.csv")
#check data has been read in properly
df.head()

#check number of rows and columns in dataset
df.shape

#create a dataframe with all training data except the target column
# X = df.drop(columns=["class"])
# X = X.drop(X.columns[1])
X = df[df.columns[2:]]
#check that the target variable has been removed
X.head()

#separate target values
y = df["class"].values
#view target values
y[0:5]

#split dataset into train and test data
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2,
                                                     random_state=1, stratify=y)

# Create KNN classifier
knn = KNeighborsClassifier(n_neighbors = 1)
# Fit the classifier to the data
knn.fit(X_train,y_train)

#show first 5 model predictions on the test data
knn.predict(X_test)[0:5]

#check accuracy of our model on the test data
knn_score = knn.score(X_test, y_test)

timestr = time.strftime("%d%m%Y-%H%M%S")

print( timestr)

# save the model to disk with accuracy and timestamp
# appended to file path
filename = './resources/model/cuckoo_model_knn_{}_acc_{}.sav'.format( timestr, round(knn_score*100, 2) )
pickle.dump(knn, open(filename, 'wb'))
