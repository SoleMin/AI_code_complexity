import pandas as pd
import sklearn
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score


def train():
    data=pd.read_csv('data/finalFeatureData.csv')
    data=data.replace('logn', 2)
    data=data.replace('n', 3)
    data=data.replace('n_square', 4)
    data=data.replace('nlogn', 5)
    y=data['complexity'].astype(int)
    x=data[['no_of_ifs','no_of_switches','no_of_loop','no_of_break','priority_queue_present','no_of_sort','hash_set_present','hash_map_present','recursion_present','nested_loop_depth','noOfVariables','noOfMethods','noOfJumps','noOfStatements']]
    x=np.array(x)
    y=np.array(y)
    x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, random_state=3)

    forest = RandomForestClassifier(n_estimators=5, random_state=2)
    forest.fit(x_train,y_train)
    y_pred=forest.predict(x_test)

    print(accuracy_score(y_test, y_pred))
    print(recall_score(y_test, y_pred,average='weighted'))
    print(precision_score(y_test, y_pred,average='weighted'))
    print(f1_score(y_test, y_pred,average='weighted'))

    sv=SVC(kernel='linear',C=1000)
    sv.fit(x_train,y_train)
    y_pred=sv.predict(x_test)

    print(accuracy_score(y_test, y_pred))
    print(recall_score(y_test, y_pred, average='weighted'))
    print(precision_score(y_test, y_pred, average='weighted'))
    print(f1_score(y_test, y_pred, average='weighted'))

    decision=DecisionTreeClassifier(random_state=164)
    decision.fit(x_train,y_train)
    y_pred=decision.predict(x_test)

    print(accuracy_score(y_test, y_pred))
    print(recall_score(y_test, y_pred, average='weighted'))
    print(precision_score(y_test, y_pred, average='weighted'))
    print(f1_score(y_test, y_pred, average='weighted'))

    lg=LogisticRegression()
    lg.fit(x_train,y_train)
    y_pred=lg.predict(x_test)

    print(accuracy_score(y_test, y_pred))
    print(recall_score(y_test, y_pred, average='weighted'))
    print(precision_score(y_test, y_pred, average='weighted'))
    print(f1_score(y_test, y_pred, average='weighted'))

    MLP=MLPClassifier(max_iter=200)
    MLP.fit(x_train,y_train)
    y_pred=MLP.predict(x_test)

    print(accuracy_score(y_test, y_pred))
    print(recall_score(y_test, y_pred, average='weighted'))
    print(precision_score(y_test, y_pred, average='weighted'))
    print(f1_score(y_test, y_pred, average='weighted'))

if __name__ == '__main__':
    train()
