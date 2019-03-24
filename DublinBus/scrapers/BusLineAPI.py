'''
Modules to deal with the API
'''
from urllib.request import urlopen
import json
import pandas as pd
from pandas.io.json import json_normalize
from sqlalchemy import create_engine

def query_API(url):
    '''
    function for interrogating the API
    '''
    #send a query to the API and decode the bytes it returns
    query = urlopen(url).read().decode('utf-8')
    #return the obtained string as a dictionary
    return json.loads(query)

def save_data_to_db(dataframe):
    #print(dataframe)
    #print(busline)
    #Assigning the engine variable values
    engine = create_engine("mysql+pymysql://Eimear:Pace2018@csstudent07:3306/dublin_bus", pool_pre_ping=True)   
    #Creating the connection with the database
    conn = engine.connect()
    #passing into scrapper functions
    print(dataframe)
    #Replaces the real time info in the RealTime table in the Amazon RDS database every 2 mins
    dataframe.to_sql(name='BusRouteOrderedStops',con=conn, if_exists='replace', index=False)
    conn.close()

def information(Info):
    '''
    funtion takes a city as a parameter and returns it a dataframe. 
    '''
    #Collect JSON Data
    #converting to a dataframe
    df = pd.DataFrame.from_dict(json_normalize(Info['results']), orient='columns')
    
    '''GENERAL RETURN INFORMATION'''
    #Prints error code if any
    #Need to implement a try catch if error code other than 0 is returned
    #print(Info["errorcode"])
    
    '''TIMETABLE INFORMATION API'''
    #Prints the timetable information for days at a given stop for a given route
    #Sunday
    #print(Info["results"][2]['departures'])
    #Mon-Fri
    #print(Info["results"][1]['departures'])
    #Saturday
    #print(Info["results"][2]['departures'])
    
    #Prints last update timestamp
    #print(Info["results"][0]['lastupdated'])
    
    '''BUS STOP INFORMATION API'''
    #Prints list of routes that service a bus stop
    #print(Info["results"][0]['operators'][0]['routes'])
    
    #Prints number of buses that service a given stop
    #print(len(Info["results"][0]['operators'][0]['routes']))
    
    #Prints bus stop name
    #print(Info["results"][0]['fullname'])
 
    #Prints bus stop ID
    #print(Info["results"][0]['displaystopid'])
    
    #Prints last update timestamp
    #print(Info["results"][0]['lastupdated'])
    
    
    '''BUS LINE INFORMATION'''
    #Prints the bus line number
#     busline=Info['route']
#     
    #Prints a list of bus stops serviced by a given line
#     RouteInfo = pd.DataFrame.from_dict(json_normalize(Info['results'][0]['stops']), orient='columns')
#     return RouteInfo[['displaystopid', 'fullname', 'latitude','longitude']], busline
  
    #Prints last update timestamp
    #print(Info["results"][0]['lastupdated'])
    
    #print(df)
    
    '''REAL TIME INFORMATION'''
    #Prints line no, destination of bus and due time for next 5 buses at at given stop
#     print(df[['route','destination','duetime']])
#     
#     #Prints last update timestamp
#     print(Info['timestamp'])

stopID = '767'
routeid='16'
operatorid='bac'
#specify the url to send to the API, in which we specify the city name and the API key
    
'''TIMETABLE INFORMATION'''
#url='https://data.smartdublin.ie/cgi-bin/rtpi/timetableinformation?type=week&stopid='+stopID+'&routeid='+routeid+'&operator='+operatorid+'&format=json'    

'''BUS STOP INFORMATION'''
url = 'https://data.smartdublin.ie/cgi-bin/rtpi/busstopinformation?operator='+operatorid+'&stopid=7663&format=json'

'''BUS LINE INFORMATION'''
# url='https://data.smartdublin.ie/cgi-bin/rtpi/routeinformation?routeid='+routeid+'&operator='+operatorid+'&format=json'

'''REAL TIME BUS INFORMATION'''
#url = 'https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid='+stopID+'&routeid='+routeid+'&operator='+operatorid+'&maxresults=5&format=json'


# #send to url to the API to get the data we want
# data = query_API(url)
# print(data)
# RealTime=pd.read_csv('PaceApp/Data/RealTime.csv',delimiter=',')
# save_data_to_db(RealTime)

#tosql, busline= information(data)
# 
# # print(data["results"][0]["stops"])
df = pd.read_csv("/home/student/DataMgt/DataAnalysis/PickleFiles/List_BusRouteStops.csv",delimiter=',')
save_data_to_db(df)
