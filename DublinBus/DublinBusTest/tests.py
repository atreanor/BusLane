import django
from django.test import TestCase, Client
import unittest
import json
from sqlalchemy import create_engine
from django.db import connection
import MySQLdb
from DublinBusTest.urls import *
from DublinBusTest.views import *
from django.urls import reverse
from DublinBusTest.viewFunctions import *
import datetime
from scipy.misc.doccer import unindent_dict
from scipy.constants.codata import unit
from django.db import connections
from django.db.utils import OperationalError
from DublinBusTest.models import *


class TestSetDatabase(unittest.TestCase):

    def test_database_connection(self):
        # Testing if database is connected by running a query and checking return type
        testQuery = Busrouteinfojoined.objects.filter(name='39')
        print(type(testQuery))
        self.assertTrue(type(testQuery) == django.db.models.query.QuerySet)
        
class TestSetApi(unittest.TestCase):
    """Testing API calls and the data returned from them"""
    
    def test_connection_weather_API(self):
        #checks if the weather API connection works
        url = "http://api.openweathermap.org/data/2.5/weather?q=dublin,ie&units=metric&appid=a87a4c45fc8819c6fd6dae5a0db2439a"
        rawData = requests.get(url)
        self.assertTrue(rawData.status_code==200)
    
    def test_city(self):
        #checks the correct city data is being returned 
        url = "http://api.openweathermap.org/data/2.5/weather?q=dublin,ie&units=metric&appid=a87a4c45fc8819c6fd6dae5a0db2439a"
        rawData = requests.get(url)
        data = json.loads(rawData.text)
        city = data['name']
        self.assertTrue(city == "Dublin")
        
    def test_connection_realtime_API(self):
        #checks connection to Real time API 
        #Passed in random stop number to test URL 
        url = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid=315&operator=bac&maxresults=5&format=json"
        rawData = requests.get(url)
        self.assertTrue(rawData.status_code == 200)
 
class TestSetViews(unittest.TestCase):
    """Tests for the views.py functions"""
       
    def test_index_connection(self):
        #checks the index template URL is loading correctly 
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_index_data(self):
        #checks the api data is returned in the correct format
        url = "http://api.openweathermap.org/data/2.5/weather?q=dublin,ie&units=metric&appid=a87a4c45fc8819c6fd6dae5a0db2439a"
        rawData=requests.get(url)
        data = json.loads(rawData.text)
        city_weather = {
            'temperature' : data['main']['temp'], 
            'icon' : data['weather'][0]['icon'],
        }
        self.assertTrue(type(city_weather) == dict)

    def test_realTimeInfo_connection(self):
        #Testing the RealTimeInfo URL is working and connecting 
        c = Client()
        response = c.get('/realTimeInfo/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
    def test_get_routes_stops_connection(self):
        #Testing the connection to the autocomplete api is working 
        c = Client() 
        response = c.post('/api/get_routes_stops/')
        self.assertEqual(response.status_code, 200)
        
        
class TestSetViewFunctions(unittest.TestCase):
    """Testing viewFunctions.py"""
    
    def test_getWeather(self):
        #testing if data is being returned and the return data type of getWeather function
        test = getWeather()
        self.assertTrue(type(test) == tuple)
        
    def test_getRealTime(self):
        #testing if data is being returned and the return data type of getRealTime function
        data = getRealTime(768)
        self.assertTrue(type(data) == list)
        
    def test_calculateFare(self):
        # testing if the logic of the fare calculator is correct 
        testOne = calculateFare(20, 70)
        testTwo = calculateFare(4, 6)
        testThree = calculateFare(4, 13)
        testFour = calculateFare(20, 5)
        self.assertTrue(testOne == "LEAP: €2.60 CASH: €3.30")
        self.assertTrue(testTwo == "LEAP: €1.50 CASH: €2.10")
        self.assertTrue(testThree == "LEAP: €2.15 CASH: €2.85")
        self.assertTrue(testFour == "Oops! You seem to have selected these stops in the wrong order. Are you sure you're going in the right direction?")
    
    def test_calculateFare_return_type(self):
        # testing that data is being returned and the return data type of calculateFare function
        testData = calculateFare(15, 60)
        self.assertTrue(type(testData) == str)
        
        
#     def test_WeatherForecast(self):
#         # testing if data is being returned and the return data type of the getWeatherForecast function
#         # Not currently working due to error - will fix 
#         now = datetime.datetime.now()
#         testDate = now.strftime("%Y-%m-%d %H:%M")
#         testData = getWeatherForecast(testDate)
#         self.assertTrue(type(testData) == tuple) 
#         
    def test_displayTime(self):
        # testing the functionality, if data is being returned, and the data type of the display_time function
        test = display_time(43200, granularity=2)
        self.assertTrue(type(test) == str)
        self.assertTrue(test == "12 hours")
        
    def test_getPeak(self):
        # testing the logic and functionality of the getPeak function
        peak1 = getPeak('09')
        peak2 = getPeak('17')
        off_peak = getPeak('14')
        self.assertTrue(peak1 == 1)
        self.assertTrue(peak2 == 1)
        self.assertTrue(off_peak == 0)
    
    def test_getPeak_return_type(self):
        # testing if data is returning and the return data type of the getPeak function
        testData = getPeak('09')
        self.assertTrue(type(testData) == int)

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSetApi, TestSetViews, TestSetViewFunctions)
    unittest.TextTestRunner().run(suite)
          
        