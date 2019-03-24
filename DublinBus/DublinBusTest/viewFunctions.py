import requests 
import json
import pandas as pd
from pandas.io.json import json_normalize
from sklearn.externals import joblib
import os
import datetime as dt
import time
from time import gmtime, strftime
from pandas.tseries.offsets import Second
from six.moves.urllib.request import urlopen
from datetime import date
from pytz import timezone
import calendar
from pymysql import TIME
from six.moves.urllib.request import urlopen
from pandas.io.json import json_normalize
import requests
import json 
import pickle
from _tracemalloc import stop
from sklearn.externals import joblib
import pandas as pd
import os
import datetime as dt
import time
from time import gmtime, strftime
from pandas.tseries.offsets import Second
from datetime import date
from pytz import timezone
import calendar
import sys
from pyleapcard import *
from pprint import pprint
from getpass import getpass
import sklearn
from sklearn.preprocessing import StandardScaler
from tornado.web import ErrorHandler


def googleDirectionsAPI(startId, endID, value, timeInSeconds):
    """
    Finds directions from one address to the other using Google API
    """
    if value == '0':
        url ='https://maps.googleapis.com/maps/api/directions/json?origin=place_id:'+startId+'&destination=place_id:'+endID+'&mode=transit&tansit_mode=bus&key=AIzaSyBUiF5d0M3ZoBV4zF_fgfswTiFXT4NeTbA'
    elif value == '1':
        url = 'https://maps.googleapis.com/maps/api/directions/json?origin=place_id:'+startId+'&destination=place_id:'+endID+'&mode=transit&tansit_mode=bus&departure_time='+timeInSeconds+'&key=AIzaSyBUiF5d0M3ZoBV4zF_fgfswTiFXT4NeTbA'
    elif value =='2':
        url = 'https://maps.googleapis.com/maps/api/directions/json?origin=place_id:'+startId+'&destination=place_id:'+endID+'&mode=transit&tansit_mode=bus&arrival_time='+timeInSeconds+'&key=AIzaSyBUiF5d0M3ZoBV4zF_fgfswTiFXT4NeTbA'
    query = urlopen(url).read().decode('utf-8')
    data = json.loads(query)
    Transit=[]
    TotalTripInfo = []
    TotalTripInfoChecker=[]
    startLocation = {"lat":data["routes"][0]["legs"][0]["start_location"]["lat"],"lon":data["routes"][0]["legs"][0]["start_location"]["lng"]}
    endLocation = {"lat":data["routes"][0]["legs"][0]["end_location"]["lat"],"lon":data["routes"][0]["legs"][0]["end_location"]["lng"]}
    for j in range(0,len(data['routes'])):
        for i in range(0,len(data["routes"][j]["legs"][0]["steps"])):
            if data["routes"][j]["legs"][0]['steps'][i]['travel_mode']=="WALKING":
                TotalTripInfo.append({"directions":data["routes"][j]["legs"][0]['steps'][i]["html_instructions"],
                                "distance":data["routes"][j]["legs"][0]['steps'][i]["distance"]["text"],
                                "duration":data["routes"][j]["legs"][0]['steps'][i]["duration"]["text"],
                                })
                TotalTripInfoChecker.append({i:"walking"})
            elif data["routes"][j]["legs"][0]['steps'][i]['travel_mode']=="TRANSIT":
                if data["routes"][j]["legs"][0]['steps'][i]['transit_details']["line"]["agencies"][0]["name"] != 'Dublin Bus':
                    break;
                else:   
                    Transit.append({"startLocation": data["routes"][j]["legs"][0]['steps'][i]['transit_details']["departure_stop"]["name"],
                                    "endLocation":data["routes"][j]["legs"][0]['steps'][i]['transit_details']["arrival_stop"]["name"],
                                    "destination":("Towards: "+str(data["routes"][j]["legs"][0]['steps'][i]['transit_details']["headsign"])),
                                    "departureTime":("Departure Time: "+str(data["routes"][j]["legs"][0]['steps'][i]['transit_details']["departure_time"]["text"])),
                                    "name":("Bus: "+str(data["routes"][j]["legs"][0]['steps'][i]['transit_details']["line"]["short_name"])),
                                    "numStops":("Number of Stops: "+str(data["routes"][j]["legs"][0]['steps'][i]['transit_details']["num_stops"]))})
                    TotalTripInfo.append({"directions":data["routes"][j]["legs"][0]['steps'][i]["html_instructions"],
                                     "distance":data["routes"][j]["legs"][0]['steps'][i]["distance"]["text"],
                                     "duration":data["routes"][j]["legs"][0]['steps'][i]["duration"]["text"],
                                     })
                    TotalTripInfoChecker.append({i:"transit"})
    return startLocation, endLocation, Transit, TotalTripInfo, TotalTripInfoChecker

def getPeak(hour):
    """
    Getting hour for peak/OffPeak
    """
    if '07' < hour < '10':
        return 1
    elif '16' < hour < '19':
        return 1
    else:
        return 0
    
def display_time(seconds, granularity=2):
    """
    Converts seconds to hours and minutes
    """
    result = []
    intervals = (('hours', 3600),('minutes', 60),('seconds', 1),)
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ' ,'.join(result[:granularity])

def calculateFare(stage1,stage2):
    """
    Calculates the fare of a joureny
    """
    if stage2 - stage1 >= 0 and stage2 - stage1 <= 3:
        fare = 'LEAP: €1.50 CASH: €2.10'
    elif stage2 - stage1 >= 4 and stage2- stage1<= 13:
        fare = 'LEAP: €2.15 CASH: €2.85'
    elif stage2 - stage1> 13:
        fare = 'LEAP: €2.60 CASH: €3.30'
    elif stage1 >= stage2: 
        fare = "Oops! You seem to have selected these stops in the wrong order. Are you sure you're going in the right direction?"
    return fare

def getWeatherForecast(datetime):
        """
        Get weather data from openweathermap
        """
        query = urlopen("http://api.openweathermap.org/data/2.5/forecast?id=7778677&APPID=e46d3193d238db99c4c25d3198720148").read().decode('utf-8')                
        #return the obtained string as a dictionary
        data = json.loads(query)
        print(len(data["list"]))
        for i in range (0, len(data["list"])):
            if data["list"][i]["dt_txt"] == datetime:
                temp = data["list"][i]["main"]["temp"]
                main = data["list"][i]["weather"][0]["main"]
                wind = data["list"][i]["wind"]["speed"]
        return temp, wind, main
    
def getRealTime(stopID):
    """
    Get the real time information for a bus stop
    """
    url = 'https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid={}&operator=bac&maxresults=5&format=json'
    r = requests.get(url.format(stopID)).json()
    r = r["results"]
    realTimeInfo = []
    if len(r)==0:
        return realTimeInfo
    elif len(r)<3:
        for i in range(len(r)):
             data = {
                'realtime' : r[i]['duetime'], 
                'route' : r[i]['route'],
            }
             realTimeInfo.append(data)
        return realTimeInfo
    else:
        for i in range(3):
             data = {
                'realtime' : r[i]['duetime'], 
                'route' : r[i]['route'],
            }
             realTimeInfo.append(data)
        return realTimeInfo
  
def callModel(route, direction, dateTime, departureValue,stopDummies1,stopDummies2):
    """
    Prepares data for models and returns results
    """
    timeDict={'05':'06','06':'06','07':'09','08':'09','09':'09','10':'12','11':'12','12':'12','13':'15','14':'15','15':'15','16':'18','17':'18','18':'18','19':'21','20':'21','21':'21','22':'00','23':'00','24':'00'}
    #Assigning values to traveldate and traveltime for model input
    #If date was selected use this date
    if dateTime != '0':
        info=dateTime.split(" ")
        traveldate=info[0]
        traveltime=info[1]
    #Otherwise use date for now
    else:
        zone='Europe/Dublin'
        other_zone=timezone(zone)
        traveldate = dt.datetime.now(other_zone).strftime('%d/%m/%Y')
        traveltime = dt.datetime.now(other_zone).strftime('%T')
             
    #Getting time of travel
    Ttime=traveltime.split(':')
    TimeinSeconds=(int(Ttime[0])*60*60)+(int(Ttime[1])*60)
               
    #Getting hour for peak/OffPeak
    hour=Ttime[0]
    peak=getPeak(hour)
             
    #Get weekday name from date input
    day=time.strftime("%A",time.strptime(traveldate, "%d/%m/%Y"))
    #Map weekday name to order of appearance in model
    daysDict={'Friday':0,'Monday':1,'Saturday':2,'Sunday':3,'Thursday':4, 'Tuesday':5,'Wednesday':6}
    #Create list for model dummies
    dayDummies = [0] * 7
    #Assign a true value to the day selected for travel
    dayDummies[daysDict[day]]=1

    #Checking if travelling now, or later to call appropriate weather function
    date=traveldate.split('/')
    #If leaving now - get weather for now
    if departureValue == '0':
        temp, wind, main = getWeather()
    #If leaving at a given time, get forecast for that time
    elif departureValue == '1': 
        hour2=timeDict[str(hour)]
        if hour2=="00":
            date[0]=int(date[0])+1
        formattedTravelDate = dt.datetime(int(date[2]), int(date[1]), int(date[0])).strftime('%Y-%m-%d')
        queriedDate=str(str(formattedTravelDate)+' '+str(hour2)+':00:00')
        temp, wind, main = getWeatherForecast(queriedDate)
    #If leaving to arrive by a given time get forecast for that time
    elif departureValue == '2':
        leaveTime = DepartureTimes[0].split(':')
        hour = leaveTime[0]
        hour2=timeDict[str(hour)]
        if hour2=="00":
            date[0]=int(date[0])+1
        formattedTravelDate = dt.datetime(int(date[2]), int(date[1]), int(date[0])).strftime('%Y-%m-%d')
        queriedDate=str(str(formattedTravelDate)+' '+str(hour2)+':00:00')
        temp, wind, main = getWeatherForecast(queriedDate)
    
    #Setting rain binary feature    
    if main =='Rain':
        rain=1
    else:
        rain=0
        
    model = joblib.load('/home/student/PaceApp_Eimear/DublinBus/DublinBusTest/PickleFiles/'+str(route)+'_'+str(direction)+'.pkl')
    scaler = joblib.load('/home/student/PaceApp_Eimear/DublinBus/DublinBusTest/PickleFiles/Scaler'+str(route)+str(direction)+'.pkl')
    First_Est=[TimeinSeconds,int(wind),temp,peak,rain]
    First_Est.extend(dayDummies)
    First_Est.extend(stopDummies1)
    
    #Preparing second run of model
    Second_Est=[TimeinSeconds,int(wind),temp,peak,rain]
    Second_Est.extend(dayDummies)
    Second_Est.extend(stopDummies2)

    Pred1=scaler.transform([First_Est])
    Pred2=scaler.transform([Second_Est])
    
    #Running predictions through model
    prediction1 = int(model.predict(Pred1))
    prediction2 = int(model.predict(Pred2))
    #Getting results
    result=prediction2-prediction1
    return result
      
def getWeather():
   """
   Get weather data from openweathermap
   """
   #send a query to the API and decode the bytes it returns
   url = 'http://api.openweathermap.org/data/2.5/weather?q={},ie&appid=a87a4c45fc8819c6fd6dae5a0db2439a'
   city = 'Dublin'
   r = requests.get(url.format(city)).json()
   temp=float(r['main']['temp'] )
   main=str(r['weather'][0]['main'])
   wind=int(r['wind']['speed'])
   return temp, wind, main