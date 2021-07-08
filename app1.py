# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 18:15:35 2021

@author: HP
"""

from numpy.lib.utils import source
from pandas._config.config import options
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from pywebio.input import *
from pywebio.output import *
from flask import Flask, send_from_directory
import sklearn
import pickle
import numpy as np
import pandas as pd
import time
model = pickle.load(open('flight-catboost_model.pkl', 'rb'))
app = Flask(__name__)

import argparse
from pywebio import start_server

def predict():
    
    values = input_group('Input Features',[
            input(label = 'Departure Date :', type = DATE,required=True, name='date_dep'),
            input(label ='Departure Time :', type = TIME,required=True, name= 'dep_time'),
            select(label = 'Please select total number of stops :',options = [0,1,2,3,4], name = 'Total_stops'),
            select(label= 'Please select the Airline :',options=['IndiGo','Air India','Multiple carriers','SpiceJet','Vistara','Air Asia','GoAir','Multiple carriers Premium economy','Vistara Premium economy'],name = 'airline'),
            select(label='Please select the Source :', options=['Chennai','Delhi','Kolkata','Mumbai','Banglore'],name='source'),
            select(label='Please select the Destination :',options= ['Cochin','Hyderabad','Delhi','Kolkata','New Delhi','Banglore'],name ='destination')
    ])
    date_dep = values['date_dep']
    Journey_day = int(pd.to_datetime(date_dep, format = "%Y-%m-%d").day)
    Journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%d").month)
    Journey_year = int(pd.to_datetime(date_dep, format ="%Y-%m-%d").year)
    
    day = pd.Timestamp(year = Journey_year, month = Journey_month, day = Journey_day).dayofweek  
       
    day_sin = np.sin(2 * np.pi * day/6)
    day_cos = np.cos(2 * np.pi * day/6)
    
    dep_time = values['dep_time']
    Dep_hour = int(pd.to_datetime(dep_time, format ="%H:%M").hour)
    Dep_min = int(pd.to_datetime(dep_time, format ="%H:%M").minute)

    Total_stops = values['Total_stops']

    airline = values['airline']
    if (airline=='Air India'):
            Air_India = 1
            GoAir = 0
            IndiGo = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 0
    elif (airline=='GoAir'):
            Air_India = 0
            GoAir = 1
            IndiGo = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 0
    elif (airline=='IndiGo'):
            Air_India = 0
            GoAir = 0
            IndiGo = 1
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 0
    elif (airline=='Multiple carriers'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Multiple_carriers = 1
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 0
    elif (airline=='Multiple carriers Premium economy'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 1
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 0
    elif (airline=='SpiceJet'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 1
            Vistara = 0
            Vistara_Premium_economy = 0   
    elif (airline=='Vistara'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 1
            Vistara_Premium_economy = 0
    elif (airline=='Vistara Premium economy'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 1
    else:
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 0
    
    Source = values['source']
    if (Source == 'Delhi'):
            s_Delhi = 1
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

    elif (Source == 'Kolkata'):
            s_Delhi = 0
            s_Kolkata = 1
            s_Mumbai = 0
            s_Chennai = 0

    elif (Source == 'Mumbai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 1
            s_Chennai = 0

    elif (Source == 'Chennai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 1

    else:
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

    destination = values['destination']
    if (destination == 'Delhi'):
            d_Delhi = 1
            d_Kolkata = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_cochin = 0

    elif (destination == 'Kolkata'):
            d_Delhi = 0
            d_Kolkata = 1
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_cochin = 0

    elif (destination == 'New Delhi'):
            d_Delhi = 0
            d_Kolkata = 0
            d_New_Delhi = 1
            d_Hyderabad = 0
            d_cochin = 0

    elif (destination == 'Hyderabad'):
            d_Delhi = 0
            d_Kolkata = 0
            d_New_Delhi = 0
            d_Hyderabad = 1
            d_cochin = 0

    elif (destination == 'Cochin'):
            d_Delhi = 0
            d_Kolkata = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_cochin = 1

    else:
            d_Delhi = 0
            d_Kolkata = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_cochin = 0

    prediction = model.predict([[Total_stops,Journey_day,Journey_month,Dep_hour,Dep_min,day_sin,day_cos,Air_India,GoAir,IndiGo,Multiple_carriers,Multiple_carriers_Premium_economy,SpiceJet,Vistara,Vistara_Premium_economy,s_Chennai,s_Delhi,s_Kolkata,s_Mumbai,d_cochin,d_Delhi,d_Hyderabad,d_Kolkata,d_New_Delhi]])
    output = round(prediction[0], 2)

    put_processbar('bar')
    for i in range(1, 11):
        set_processbar('bar', i / 10)
        time.sleep(0.1)
   
    if output < 0:
        put_text("Sorry Invalid Inputs")

    else:
        if (airline=='Air India'):
                put_image(open('airlines/Air_india.jpg', 'rb').read())
        elif (airline=='GoAir'):
                put_image(open('airlines/Go Air.jpg', 'rb').read())
        elif (airline=='IndiGo'):
                put_image(open('airlines/indi-go-banner.jpg', 'rb').read())
        elif (airline=='SpiceJet'):
                put_image(open('airlines/spicejet.jpg', 'rb').read())
        elif (airline=='Vistara'):
                put_image(open('airlines/vistara.jpg', 'rb').read())
        elif (airline=='Vistara Premium economy'):
                put_image(open('airlines/vistara.jpg', 'rb').read())
        elif (airline=='Air Asia'):
                put_image(open('airlines/air_asia.jpg', 'rb').read())
        
        put_text('Predicted price of your flight is ',output ,'rupees').style('color: black; font-size: 25px')

    
app.add_url_rule('/tool', 'webio_view', webio_view(predict),
            methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(predict, port=args.port)

#app.run(host='localhost', port=80, debug=True)
#visit http://localhost/tool to open the PyWebIO application.