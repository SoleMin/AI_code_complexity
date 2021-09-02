import csv
import numpy as np
from sklearn.cluster import KMeans
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import BernoulliNB
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
class Naive_Bayes():
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
			if(complexity==('n' or 'n_square')):
				continue
			for i in features:
				i = (int)(i)
			self.arr_names.append(name)
			self.arr.append(features)
			self.arr_complexities.append(complexity_dictionary[complexity])

		self.arr = np.asarray(self.arr, dtype=float)
		self.arr_complexities = np.asarray(self.arr_complexities)

		# shuffle the data
		self.arr, self.arr_complexities, self.arr_names = shuffle(self.arr, self.arr_complexities, self.arr_names, random_state=0)
	def train(self):
		no_of_variables = 14
		scores = []
		precisions = []
		recalls = []

		for i in range(1, no_of_variables):
			array = self.arr[:, :i]
			score = []
			prec = []
			rec = []
			kf = KFold(n_splits=5, shuffle=True)
			for train_index, test_index in kf.split(array, self.arr_complexities):
				X_train, X_test = array[train_index], array[test_index]
				y_train, y_test = self.arr_complexities[train_index], self.arr_complexities[test_index]

				gnb = BernoulliNB()
				gnb.fit(X_train, y_train)
				y_predicted = gnb.predict(X_test)
				# print(y_predicted)
				acc_score = accuracy_score(y_test, y_predicted)
				score.append(acc_score)
				prec.append(precision_score(y_test, y_predicted, average='weighted'))
				rec.append(recall_score(y_test, y_predicted, average='weighted'))
			scores.append(max(score))
			precisions.append(max(prec))
			recalls.append(max(rec))

		plt.plot(scores)
		plt.savefig('nb_vs_vaiable_count.png')
		print('Scores: ', scores)
