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
from sklearn.decomposition import PCA
import scikitplot as skplt
from sklearn.utils import shuffle
from sklearn.metrics import precision_score, recall_score


complexity_dictionary = {'n':0, 'n_square':1, 'logn':2, 'nlogn':3, 'sqrtn':4, 'n_cube':5, 'n_squarelogn':6, '1':7, 'logn_square':8}
color_mapping = {0:'r', 1:'g', 2:'b', 3:'y', 4:'m', 5:'c', 6:'k', 7:'lime', 8:'orange'}

class DecisionTree():
	def __init__(self,data):
		self.array = []
		self.arr_complexities = []
		self.arr_names = []

		count = 0

		for row in data:
			count = count + 1
			if (count == 1):
				continue
			name = row[-1]
			features = row[0:13]
			complexity = row[-2]
			# if(complexity==('nlogn' or 'logn')):
			# 	continue
			for i in features:
				i = (int)(i)
			self.arr_names.append(name)
			self.array.append(features)
			self.arr_complexities.append(complexity_dictionary[complexity])


	def train(self):
		arr = np.asarray(self.array, dtype=float)
		arr_complexities = np.asarray(self.arr_complexities)

		no_of_variables = 14
		scores = []
		precisions = []
		recalls = []

		# shuffle the data
		arr, arr_complexities = shuffle(arr, arr_complexities, random_state=0)


		for i in range(1, no_of_variables):
			array = arr[:, :i]
			score = []
			prec = []
			rec = []
			print(array.shape)

			kf = KFold(n_splits=5, shuffle=True)
			for train_index, test_index in kf.split(array, arr_complexities):
				X_train, X_test = array[train_index], array[test_index]
				y_train, y_test = arr_complexities[train_index], arr_complexities[test_index]
				clf = tree.DecisionTreeClassifier(random_state=0, max_depth=5)
				clf = clf.fit(X_train, y_train)
				y_predicted = clf.predict(X_test)
				acc_score = accuracy_score(y_test, y_predicted)
				score.append(acc_score)
				prec_ = precision_score(y_test, y_predicted, average='weighted')
				rec_ = recall_score(y_test, y_predicted, average='weighted')
				prec.append(prec_)
				rec.append(rec_)
			scores.append(max(score))
			precisions.append(max(prec))
			recalls.append(max(rec))

		print('Scores: ', scores)
		print('Precisions: ', precisions)
		print('Recalls: ', recalls)
		plt.plot(scores)
		plt.savefig('./decisiontree_vs_variable_count.png')