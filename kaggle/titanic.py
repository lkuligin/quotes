#!/usr/bin/env python
# coding: utf8
"""
heuristis for https://www.kaggle.com/c/titanic
"""

import numpy as np
import pandas

def simple_heuristic(file_path):
	predictions = {}
	df = pandas.read_csv(file_path)
	#print df.head()
	for passenger_index, passenger in df.iterrows():
		passenger_id = passenger['PassengerId']
		if passenger['Sex'] == 'female':
			predictions[passenger_id] = 1
		elif passenger['Age'] < 16 and passenger['Pclass'] == 1:
			predictions[passenger_id] = 1
		elif passenger['Age'] < 16 and passenger['Pclass'] == 2:
			predictions[passenger_id] = 1
			else:
			predictions[passenger_id] = 0
	return predictions
	
	
if __name__ == '__main__':
	path = "C:/Users/kuligin/Downloads/test.csv"
	pathTrain = "C:/Users/kuligin/Downloads/train.csv"
	trainData = pandas.read_csv(pathTrain)
	#print len(trainData)
	trainData['Age1'] = trainData['Age'] < 17
	print trainData.groupby(['Sex', 'Age1', 'Pclass', 'Survived'])['PassengerId'].count()
	#print trainData.groupby(['Pclass', 'Sex', 'Survived'])['PassengerId'].count()
	#print trainData.head()
	simple_heuristic(path)
