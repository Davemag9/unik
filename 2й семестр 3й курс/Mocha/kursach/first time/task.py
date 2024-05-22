import time
from sklearn.datasets import load_digits

from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn import datasets
from sklearn.metrics import accuracy_score,confusion_matrix # metrics error
from sklearn.model_selection import train_test_split # resampling method

def task(df_to_check):
    predictions_val = knn.predict(df_to_check[0])
    print('KNN Accuracy: %.3f' % accuracy_score(df_to_check[1], predictions_val))

