import pandas as pd
from codes import decisiontree,kmeans,knn,mlp_classifier,logistic_regression,naive_bayes,svm,randomforest
from AST import feature_Extractor
import numpy as np
def feature_base():

    arr = np.zeros(13)

    temp_data=pd.read_csv('data/finalFeatureData.csv').dropna()
    data_name=temp_data['file_name'].reset_index(drop=True)
    data_complexity=temp_data['complexity'].reset_index(drop=True)

    for num,i in enumerate(data_name):
        # if i!='1513.java' and i!='35.java' and i!='362.java' and i!='774.java':
            arr=np.vstack([arr,feature_Extractor(i)])

    arr=arr[1:,:]
    data=pd.DataFrame(arr)
    data =pd.concat([data,data_complexity,data_name],axis=1).to_numpy()

    decision=decisiontree.DecisionTree(data)
    decision.train()

    # error
    # KM=kmeans.Kmeans(data)
    # KM.train()

    KN=knn.KNN(data)
    KN.train()

    logistic=logistic_regression.Logistic_Regression(data)
    logistic.train()

    mlp=mlp_classifier.MLP(data)
    mlp.train()

    NV=naive_bayes.Naive_Bayes(data)
    NV.train()
    # error
    # random=randomforest.Random_Forest(data)
    # random.train()

    sv=svm.SVM(data)
    sv.train()
def graph2vec_base():

    temp_data = pd.read_csv('data/finalFeatureData.csv').dropna()
    feautre_data=pd.read_csv('features/nci2.csv')
    arr = np.zeros(1024)

    data_name = temp_data['file_name'].reset_index(drop=True)
    data_complexity = temp_data['complexity'].reset_index(drop=True)

    for num, i in enumerate(data_name):
        # if i!='1513.java' and i!='35.java' and i!='362.java' and i!='774.java':
        arr = np.vstack([arr, feautre_data[feautre_data['type']==int(i.strip(".java"))].to_numpy().reshape(-1)[1:]])
    arr=arr[1:,:]
    data=pd.DataFrame(arr)
    data =pd.concat([data,data_complexity,data_name],axis=1).to_numpy()

    sv=svm.SVM(data)
    sv.train()
if __name__ == '__main__':
    graph2vec_base()
