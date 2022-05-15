import numpy as np
from lightfm import LightFM
import pandas as pd
from scipy.sparse import csr_matrix
from flask import Flask, render_template, request, redirect, url_for, jsonify
from geopy.geocoders import Nominatim
from city_data import City
import http.client
import json
from covid_data import get_data, get_covid_data
import os

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method=='GET':
        city_list_dic = {"city_list":city_list}
        return render_template('home1.html',data=city_list_dic)
    if request.method=='POST':
        user_input = [request.form.get('city1'),request.form.get('city2'),request.form.get('city3'),request.form.get('city4'),request.form.get('city5')]
        # cities is a list of cities, each city is in format "city_name, state", e.g., "Atlanta, GA"
        city_index, cities = recommend(data,user_input)

        #print(city_name)
        # citi_name is a list of cities, each city only has its name, e.g., "Atlanta"
        city_name = [c for c in cities]
        city_name_2 = [c.split(',')[0] for c in cities]

        gps = Nominatim(user_agent="app")
        city_gps = {
            city_name[0]: [gps.geocode(city_name[0]).latitude,gps.geocode(city_name[0]).longitude],
            city_name[1]: [gps.geocode(city_name[1]).latitude,gps.geocode(city_name[1]).longitude],
            city_name[2]: [gps.geocode(city_name[2]).latitude,gps.geocode(city_name[2]).longitude],
            city_name[3]: [gps.geocode(city_name[3]).latitude,gps.geocode(city_name[3]).longitude],
            city_name[4]: [gps.geocode(city_name[4]).latitude,gps.geocode(city_name[4]).longitude]
        }

        # get covid data (risk levels) for each city
        covid_data = get_data()
        # e.g., "Atlanta": {'CDC Transmission Level': 2, 'Overall Risk Level': 2, 'Case Density': 2, 'Infection Rate': 0, 'Test Positivity Ratio': 0}
        city_covid_info = {}
        for i in range(5):
            city_covid_info[city_name[i]] = get_covid_data(covid_data,cities[i])
        print(city_covid_info)

        city_getter = City()

        city_info = {
            city_name_2[0]: city_getter.return_data(city_name_2[0]),
            city_name_2[1]: city_getter.return_data(city_name_2[1]),
            city_name_2[2]: city_getter.return_data(city_name_2[2]),
            city_name_2[3]: city_getter.return_data(city_name_2[3]),
            city_name_2[4]: city_getter.return_data(city_name_2[4])
        }
        #print(city_name)

        return render_template('home2.html', data = city_gps, data2 = city_info, covid_data = city_covid_info)

        # return jsonify(city_gps)
@app.route('/us-states.js')
def script1():
    return render_template('us-states.js')

@app.route('/auto-complete.js')
def script2():
    return render_template('auto-complete.js')


def recommend(data,user_input):
    covid_data = get_data()
    city_list = list(data.columns)  # list of city
    row_num = data.shape[0]
    col_num = data.shape[1]
    new_data = [0]*col_num # create and append the new user record to the data set
    for i in range(len(user_input)):
        new_data[city_list.index(user_input[i])]=1
    new_data = pd.Series(new_data,city_list)
    new_data_df = pd.DataFrame(new_data).transpose()
    data = data.append(new_data_df, ignore_index=True)
    data_compact = csr_matrix(data) # compact data
    model = LightFM(loss = 'warp').fit(data_compact) # build model
    item = list(range(col_num)) # index of item
    predict_score = model.predict(row_num, item) # predict for the new user
    covid_score = np.array([get_covid_data(covid_data,c)['Overall Risk Level'] for c in city_list])
    city_index = np.argsort(predict_score*(5-covid_score))[::-1][0:10]
    cities = []
    for i in city_index:
        if not city_list[i] in user_input:
            cities = cities + [city_list[i]]
    return city_index, cities
    # output preidct city for user
    # show the 5 best suitable city



if __name__ == '__main__':
    data = pd.read_csv("user_data.csv")
    #data.drop(["userID"],axis = 1, inplace = True) # drop user id
    city_list = list(data.columns)
    app.run()
    input("Press Enter to exit…")

