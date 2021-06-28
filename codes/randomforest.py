import csv
import numpy as np
from sklearn.cluster import KMeans
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn import svm
import matplotlib
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.model_selection import KFold
from scipy.stats import mode
from sklearn.utils import shuffle
from sklearn.metrics import precision_score, recall_score
from sklearn.feature_selection import SelectFromModel


complexity_dictionary = {'n':0, 'n_square':1, 'logn':2, 'nlogn':3, '1':4}
color_mapping = {0:'r', 1:'g', 2:'b', 3:'y', 4:'m'}
file_to_complexity_mapping = {}
class Random_Forest():
	def __init__(self,data):
		self.arr = []
		self.arr_complexities = []
		self.arr_names = []
		count = 0
		for row in data:
			count = count + 1
			if(count==1):
				continue
			name = row[-1]
			features = row[0:13]
			complexity = row[-2]
			if(complexity=='n'  or complexity=='1' or complexity=='logn'):
				continue
			for i in features:
				i = (int)(i)
			self.arr_names.append(name)
			self.arr.append(features)
			self.arr_complexities.append(complexity_dictionary[complexity])

		self.arr = np.asarray(self.arr).reshape(-1, 1)
		self.arr_complexities = np.asarray(self.arr_complexities)

		# shuffle the data
		self.arr, self.arr_complexities, self.arr_names = shuffle(self.arr, self.arr_complexities, self.arr_names, random_state=0)

	def train(self):
		no_of_variables = 14
		scores = []
		precisions = []
		recalls = []

		X_train, X_test = self.arr[:(int)(0.9*len(self.arr))], self.arr[(int)(0.9*len(self.arr)):]
		y_train, y_test = self.arr_complexities[:(int)(0.9*len(self.arr))], self.arr_complexities[(int)(0.9*len(self.arr)):]
		train_names = self.arr_names[:(int)(0.9*len(self.arr))]
		test_names = self.arr_names[(int)(0.8*len(self.arr)):]

		classifier = RandomForestClassifier(n_estimators=100, max_depth=4, random_state=0)
		classifier.fit(X_train, y_train)
		y_predicted = classifier.predict(X_test)
		acc_score = accuracy_score(y_test, y_predicted)

		print(y_test)
		print(y_predicted)