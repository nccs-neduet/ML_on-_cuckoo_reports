import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


#read in the data using pandas
df = pd.read_csv("./resources/feature_frame.csv")
#check data has been read in properly
df.head()

#check number of rows and columns in dataset
df.shape

#create a dataframe with all training data except the target column
X = df.drop(columns=["class"])
X = X.drop(X.columns[1])
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
knn = KNeighborsClassifier(n_neighbors = 3)
# Fit the classifier to the data
knn.fit(X_train,y_train)

#show first 5 model predictions on the test data
knn.predict(X_test)[0:5]