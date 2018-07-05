import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import time

from operator import itemgetter
from ast import literal_eval
from distance_ops import computeDTW

from sklearn.utils import shuffle
from sklearn import preprocessing
from sklearn.model_selection import KFold
from my_knn_classifier import knn_find_stats,knn_predict

if __name__ =="__main__":

	#read dataset
	train = pd.read_csv(
		'./datasets/train_set.csv',
		converters={"Trajectory": literal_eval})

	test = pd.read_csv(
		'./datasets/test_set_a2.csv',
		sep = '|',
		converters=dict(Trajectory=literal_eval))

	trainTraj = train['Trajectory']
	trainJour = train['journeyPatternId']

	testTraj = test['Trajectory']

	#creating a random train subset
	subtrain = train.sample(frac=1)
	sublen = int(len(train)/10)
	subtrain = subtrain[:sublen]
	stTraj = subtrain['Trajectory']

	le=preprocessing.LabelEncoder()
	le.fit(subtrain['journeyPatternId'])
	y = le.transform(subtrain['journeyPatternId'])

	cvm = KFold(n_splits=10,shuffle=False)

	k=5
	accuracy = knn_find_stats(np.array(stTraj), y, k, cvm)
	print 'accuracy:',accuracy

	le=preprocessing.LabelEncoder()
	le.fit(train['journeyPatternId'])
	y = le.transform(train['journeyPatternId'])
#							Xtrain			test			  ytrain
	y_pred = knn_predict(np.array(trainTraj),np.array(testTraj),	y	,k)

	test_journeyPatternId = le.inverse_transform(y_pred)
	#print test_journeyPatternId

	test_ids = [i+1 for i in range(len(test.Trajectory))]

	test_ids = np.array(test_ids)

	mydict = {'Test_Trip_ID':test_ids,
			 'Predicted_JourneyPatternId':test_journeyPatternId}

	df = pd.DataFrame.from_dict(data=mydict)
	df = df[['Test_Trip_ID','Predicted_JourneyPatternId']]#reordering
	df.to_csv('testSet_JourneyPatternIds.csv',sep='\t',index=False)


