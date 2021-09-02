from sklearn.linear_model import LogisticRegression
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
from sklearn.decomposition import PCA
from sklearn.metrics import precision_recall_curve
from sklearn.feature_selection import SelectKBest, chi2
import scikitplot as skplt
from sklearn.metrics import precision_score, recall_score


complexity_dictionary = {'n':0, 'n_square':1, 'logn':2, 'nlogn':3, '1':4}
color_mapping = {0:'r', 1:'g', 2:'b', 3:'y', 4:'m'}
file_to_complexity_mapping = {}
rejected_names = []

class Logistic_Regression():
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
			if(complexity==('nlogn' or 'logn')):
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

		count = 0

		no_of_variables = 14
		scores = []
		precisions = []
		recalls = []

		for i in range(1, no_of_variables):
			array = self.arr[:, :i]
			acc_score = []
			prec = []
			rec = []
			kf = KFold(n_splits=5, shuffle=True)
			for train_index, test_index in kf.split(array, self.arr_complexities):
				count += 1
				X_train, X_test = array[train_index], array[test_index]
				y_train, y_test = self.arr_complexities[train_index], self.arr_complexities[test_index]
				clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial').fit(X_train, y_train)
				y_predicted = clf.predict(X_test)
				acc_score .append(accuracy_score(y_test, y_predicted))
				prec.append(precision_score(y_test, y_predicted, average='weighted'))
				rec.append(recall_score(y_test, y_predicted, average='weighted'))
			score = max(acc_score)
			scores.append(score)
			precisions.append(max(prec))
			recalls.append(max(rec))

		print('Scores: ', scores)
		plt.plot(scores)
		plt.savefig('./logistic_vs_variable_count.png')
