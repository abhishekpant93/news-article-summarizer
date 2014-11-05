import csv
import numpy as np
from sklearn import linear_model


data = []
target = []
with open('../resource/db.csv', 'rb') as f:
	mycsv = csv.reader(f)
	for row in mycsv:
		data.append(np.array([float(row[1]), float(row[2]), float(row[3]), float(row[4])]))
		target.append(float(row[0]))

regr = linear_model.LinearRegression()
regr.fit(data, target)
print('Coefficients: \n', regr.coef_)
