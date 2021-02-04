import requests
from datetime import date
import time
import pandas as pd
import numpy as np
from sklearn import linear_model
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import csv

mins = []
maxs = []
avgs = []
abbrs = []
hums = []
pressure = []
wind = []
predhum = []
predpress = []
predwind = []
predhum1 = []
predpress1 = []
predwind1 = []
predhum2 = []
predpress2 = []
predwind2 = []

temp = 0
x = 20
currentDate = date.today()
currentYear = currentDate.strftime("%Y")
currentYear = int(currentYear)
currentMonth = currentDate.strftime("%m")
currentDay = currentDate.strftime("%d")


def fetch():
    req1 = requests.get("https://60089720309f8b0017ee62d5.mockapi.io/ID")
    result1 = req1.json()
    count1 = len(result1)
    data1 = result1[count1 - 1]
    woeids1 = data1["woeid"]
    print(woeids1)
    return woeids1


def pre(woeid):
    for k in range(3):
        for j in range(1, 4):
            req = requests.get("https://www.metaweather.com/api/location/" + str(woeid) + "/" + str(
                2020-k) + "/" + str(int(currentMonth) + j) + "/" + currentDay + "/")
            result = req.json()
            data = result[0]
            hum = int(round(data["humidity"]))
            pres = int(round(data["air_pressure"]))
            ws = int(round(data["wind_speed"]))
            if j == 1:
                predhum.append(hum)
                predpress.append(pres)
                predwind.append(ws)

            if j == 2:
                predhum1.append(hum)
                predpress1.append(pres)
                predwind1.append(ws)

            if j == 3:
                predhum2.append(hum)
                predpress2.append(pres)
                predwind2.append(ws)
            print("predicting")





def reg(humid, pr, wd):
    filename = 'Regressor_model4.sav'
    myRegModel = pickle.load(open(filename, 'rb'))
    x = myRegModel.predict([[humid, pr, wd]])
    return round(int((x)))


def post():
    avghum = sum(predhum) / len(predhum)
    avgwind = sum(predwind) / len(predwind)
    avgpres = sum(predpress) / len(predpress)

    avghum1 = sum(predhum1) / len(predhum1)
    avgwind1 = sum(predwind1) / len(predwind1)
    avgpres1 = sum(predpress1) / len(predpress1)

    avghum2 = sum(predhum2) / len(predhum2)
    avgwind2 = sum(predwind2) / len(predwind2)
    avgpres2 = sum(predpress2) / len(predpress2)
    data = {
        "temp1": reg(avghum, avgpres, avgwind),
        "temp2": reg(avghum1, avgpres1, avgwind1),
        "temp3": reg(avghum2, avgpres2, avgwind2)
    }

    requests.post("https://60089720309f8b0017ee62d5.mockapi.io/flutter", data=data)

    print("posted succesfully")



while (True):
    try:
        x = fetch()
    except:
        print("can't fetch")
    time.sleep(0.5)
    if (x != temp):
        del predpress[:]
        del predwind[:]
        del predhum[:]
        del predpress1[:]
        del predwind1[:]
        del predhum1[:]
        del predpress2[:]
        del predwind2[:]
        del predhum2[:]
        pre(x)
        post()
    temp = x

"""df = pd.DataFrame(data={"temp": avgs, "humidity": predhum, "pressure": predpress, "wind": predwind})
df.to_csv("file.csv", sep=',', index=False)
X = df[["humidity", "pressure", "wind"]]
y = df[["temp"]]

regressor = linear_model.LinearRegression()
regressor.fit(X,y)

filename='Regressor_model.sav'
pickle.dump(regressor, open(filename, 'wb'))"""
