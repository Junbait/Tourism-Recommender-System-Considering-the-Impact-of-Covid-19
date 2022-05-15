import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from flask import Flask, render_template, request, redirect, url_for, jsonify
import http.client
import json

def get_data():
    # obtain covid_data
    api_key = "4271ef2e0ab74f70994fb6b9058d11e5"
    conn = http.client.HTTPSConnection("api.covidactnow.org")
    conn.request("GET", "/v2/states.json?apiKey=" + api_key)
    response = conn.getresponse().read().decode('utf-8')
    data = json.loads(response)
    data = pd.DataFrame.from_dict(data)
    # select statistics
    covid_data = data[['state','metrics','riskLevels','cdcTransmissionLevel']]
#    covid_data['Case Density'] = [d.get('caseDensity') for d in covid_data.metrics]
#    covid_data['Infection Rate'] = [d.get('infectionRate') for d in covid_data.metrics]
#    covid_data['Test Positivity Ratio'] = [d.get('testPositivityRatio') for d in covid_data.metrics]
    covid_data = pd.concat([covid_data.drop(['metrics','riskLevels'], axis=1), covid_data.riskLevels.apply(pd.Series)],axis=1)
#    covid_data['Case Density']= list(zip(covid_data['Case Density'], covid_data['caseDensity']))
#    covid_data['Infection Rate']= list(zip(covid_data['Infection Rate'], covid_data['infectionRate']))
#    covid_data['Test Positivity Ratio']= list(zip(covid_data['Test Positivity Ratio'], covid_data['testPositivityRatio']))
    covid_data['Case Density']= covid_data['caseDensity']
    covid_data['Infection Rate']= covid_data['infectionRate']
    covid_data['Test Positivity Ratio']= covid_data['testPositivityRatio']
    covid_data = covid_data.rename(columns={'cdcTransmissionLevel':'CDC Transmission Level','overall':'Overall Risk Level'})
    covid_data = covid_data.drop(['testPositivityRatio','caseDensity','contactTracerCapacityRatio','infectionRate','icuCapacityRatio'],axis=1)
    return covid_data

def get_covid_data(covid_data, city):
    # return the covid-data corresponding to the state that the city belongs to
    state = city.split(',')[-1].replace(" ","")
    return covid_data[covid_data.state == state].iloc[:,1:].to_dict(orient='records')[0]
