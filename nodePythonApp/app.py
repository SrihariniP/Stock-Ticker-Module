import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
yf.pdr_override()
from pandas_datareader import data as wb
from keras.models import load_model
from datetime import date
import json
import sys


def number_of_days(date_1, date_2):  
    return (date_2 - date_1).days 

#user_input = sys.argv[1]
user_input = 'AAPL'


# Loading the data
date_start = date(2010, 1, 1)
date_today = date.today()
symbol = user_input
data_source = 'yahoo'

df = wb.DataReader(symbol, date_start, date_today, data_source)

#print("df = \n")
#print(df, "\n")


#Splitting the data into training and testing

data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.9)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.9):int(len(df))])

x_plot_vals = df.index[int(len(df)*0.9):int(len(df))]
#print("x_plot_vals = ", x_plot_vals)

#print(data_training.shape)
#print(data_testing.shape)


# Loading the scaler and scaling data

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range = (0,1))

data_training_array = scaler.fit_transform(data_training)

# Loading the model

model = load_model('keras_model.h5')

#Testing Part

past_100_days = data_training.tail(100)
final_df = pd.concat([past_100_days, data_testing], ignore_index = True)


input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)

# Making Predictions

y_predicted = model.predict(x_test)

#scaler = scaler.scale_

#scale_factor = 1/scaler
y_predicted = scaler.inverse_transform(y_predicted)
y_test = scaler.inverse_transform(y_test.reshape(-1,1))

#print("y_predicted = ", y_predicted)
#print("y_test = ", y_test)

data_points = []

no_of_days = number_of_days(date_start, date_today)

data_points = []

count = 0

for i in x_plot_vals:
    xval = [int(i.strftime("%Y")), int(i.strftime("%m")), int(i.strftime("%d"))]
    yval = [(y_test[count][0]).astype(float), (y_predicted[count][0]).astype(float)]
    count+=1
    json_element = {'x': xval, 'y': yval}
    data_points.append(json_element)


#print("data_points = ", data_points)

json_data = json.dumps(data_points)

print(json_data, flush=True)