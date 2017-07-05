import pandas as pd
import numpy as np
from datetime import datetime

sphist = pd.read_csv("sphist.csv")

colums = ["Date", "Open", "High", "Low", "Close", "Volume", "Adj Close"]

#converting to pandas dataframe
sphist["Date"] = pd.to_datetime(sphist["Date"])

# order by date
sphist_ordered = sphist.sort_values("Date", ascending=True)

# adding index to dataframe
sphist_ordered["index"] = range(0,sphist_ordered.shape[0],1)
sphist_ordered.set_index(["index"])

# select indicators
Data_Mean_5_Days = pd.rolling_mean(sphist_ordered.Close, window=5).shift(1)

Data_Mean_365_Days = pd.rolling_mean(sphist_ordered.Close, window=365).shift(1)

Data_Mean_Ratio = Data_Mean_5_Days/Data_Mean_365_Days

Data_Std_5_Days = pd.rolling_std(sphist_ordered.Close, window=5).shift(1)

Data_Std_365_Days = pd.rolling_std(sphist_ordered.Close, window=365).shift(1)

Data_Std_Ratio = Data_Std_5_Days/Data_Std_365_Days

#adding columns to dafarame
sphist_ordered["Data_Mean_5_Days"] = Data_Mean_5_Days
sphist_ordered["Data_Mean_365_Days"] = Data_Mean_365_Days
sphist_ordered["Data_Mean_Ratio"] = Data_Mean_Ratio
sphist_ordered["Data_Std_5_Days"] = Data_Std_5_Days
sphist_ordered["Data_Std_365_Days"] = Data_Std_365_Days
sphist_ordered["Data_Std_Ratio"] = Data_Std_Ratio

#selecting train data
less_than_2012 = (sphist_ordered["Date"] < datetime(year=2013, month=1, day=1))

more_than_1949 = sphist_ordered["Date"] >= datetime(year=1950, month=1, day=1)

train_data = sphist_ordered[less_than_2012 & more_than_1949]

train_data.dropna(axis=0, inplace=True)

#selecting test data
less_than_2015 = (sphist_ordered["Date"] < datetime(year=2016, month=1, day=1))

more_than_2013 = sphist_ordered["Date"] >= datetime(year=2013, month=1, day=1)

test_data = sphist_ordered[less_than_2015 & more_than_2013]

test_data.dropna(axis=0, inplace=True)

#import linear regression model for predictions
from sklearn.linear_model import LinearRegression
model = LinearRegression()

#select features
features = ["Data_Mean_5_Days",
"Data_Mean_365_Days",
"Data_Mean_Ratio",
"Data_Std_5_Days",
"Data_Std_365_Days",
"Data_Std_Ratio"]

# select data for training and testing
x = train_data[features]
x_test = test_data[features]
# select Close as we want to know what closing price will be
y = train_data["Close"]
y_test = test_data["Close"]

#fit data to the model
model.fit(x, y)

#make prediction
prediction = model.predict(x_test)

MAE = sum(abs(prediction - y_test))/len(prediction)

print(MAE)
print(model.score(x, y))