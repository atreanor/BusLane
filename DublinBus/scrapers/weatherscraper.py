import requests
import json
import time 
import pymysql
import pandas as pd
from pymysql.err import IntegrityError
from time import sleep, strftime, gmtime
import pymysql.cursors
import datetime
import sys
import requests 
from six.moves.urllib.request import urlopen
import json
import pandas as pd
from pandas.io.json import json_normalize
from sklearn.externals import joblib
import pandas as pd
import os
import datetime as dt
import time
from time import gmtime, strftime
from pandas.tseries.offsets import Second
from six.moves.urllib.request import urlopen
from datetime import date
from pytz import timezone
import calendar
import sys

# def dbConnect():
#     
#     """Function to connect to the database"""
#     
#     try:
#         db = pymysql.connect(
#             host='csserver07',
#             user='Ciara',
#             passwd='Pace2018',
#             db='dublin_bus'
#         )
#         
#     except Exception as e: 
#         sys.exit("Cannot connect to database")
#     return db
#     
# def insertDb(data, db):
#     
#     """Function to insert the data into the database"""
#     
#     try:
#         cursor = db.cursor()
#         
#         add_weather = ("REPLACE INTO owm_forecast__data "
#                     "(temp, temp_min, temp_max, main, description, clouds, wind_speed, wind_deg, date) "
#                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
#         
#         cursor.execute(add_weather, data)
#         db.commit()
#         
#     except Exception as e: 
#         template = "Insert An exception of type {0} occurred. Arguments:\n{1!r}"
#         message = template.format(type(e).__name__, e.args)
#         print(message)
# 
# def main():
# 
#     """Function to connect to the API and call the above functions to run the scraper"""
# 
#     url = "http://api.openweathermap.org/data/2.5/forecast?q=dublin,ie&units=metric&appid="
#     db = dbConnect()
#     print("Connected!")
#     while True: 
#         rawData = requests.get(url)
#         print(rawData.status_code)
# 
#         if rawData.status_code == 200:
#             data = json.loads(rawData.text)
#             print("Working")
#             id = data['city']['country']
#             print(id)
# 
# 
# 
#             data_list = data['list'][2]
#             
#         
#             temp = data['list'][0]['main']['temp']
#             temp_min = data['list'][0]['main']['temp_min']
#             temp_max = data['list'][0]['main']['temp_max']
#             main = data['list'][0]['weather'][0]['main']
#             description = data['list'][0]['weather'][0]['description']
#             clouds = data['list'][0]['clouds']['all']
#             wind_speed = data['list'][0]['wind']['speed']
#             wind_deg = data['list'][0]['wind']['deg']
#             date = data['list'][0]['dt']
#         
#             
#             
#             data = [temp, temp_min, temp_max, main, description, clouds, wind_speed, wind_deg, date]
#             insertDb(data, db)
# 
#         
#         print('sleeping') 
#         time.sleep(1800)
#            
# if __name__ == "__main__":
#     main()
    

"""Get weather data from openweathermap"""
#send a query to the API and decode the bytes it returns
url = 'http://api.openweathermap.org/data/2.5/weather?q={},ie&appid=a87a4c45fc8819c6fd6dae5a0db2439a'
city = 'Dublin'
r = requests.get(url.format(city)).json()
temp=float(r['main']['temp'] )
main=str(r['weather'][0]['main'])
wind=int(r['wind']['speed'])
print(r)

#         df = pd.DataFrame.from_dict(json_normalize(data['list'][0]['weather']), orient='columns')
#         for i in range(1,data["cnt"]):
#             df1 = pd.DataFrame.from_dict(json_normalize(data['list'][i]['weather']), orient='columns')
#             df = df.append(df1, ignore_index=True)
#         df2 = pd.DataFrame.from_dict(json_normalize(data['list']), orient='columns')
#         df2.rename(columns={'main.temp': 'temp'}, inplace=True)
#         temp = df2['temp']
#         df2['temp'] = temp.round()
#         df2.rename(columns={'wind.speed': 'wind_speed'}, inplace=True)
#         dataframe = pd.concat([df, df2], axis=1)
#         miniframe= dataframe.loc[(dataframe.dt_txt ==datetime)]
#         temp = miniframe.at[0,'temp']
#         wind= miniframe.at[0,'wind_speed']
#         main = miniframe.at[0,'main']
#         return temp, wind, main
