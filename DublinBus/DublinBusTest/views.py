from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django import forms
from DublinBusTest.forms import *
from DublinBusTest.models import *
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
from django.db import connection
from pyleapcard import *
from pprint import pprint
from getpass import getpass
import sklearn
from sklearn.preprocessing import StandardScaler
from DublinBusTest.viewFunctions import *
from tornado.web import ErrorHandler


def index(request):
    """Code to render the index page with the data from the database displayed"""
    # Data from https://openweathermap.org/api
    
    # API call - reads in weather and stores relevant information in a dict
    url = 'http://api.openweathermap.org/data/2.5/weather?q={},ie&units=metric&appid=a87a4c45fc8819c6fd6dae5a0db2439a'
    city = 'Dublin'
    r = requests.get(url.format(city)).json()
    if r['cod'] == 401:
        city_weather = {
        'temperature' : "Currently not available", 
        'icon' : "",
        }
    else:
        city_weather = {
        'temperature' : int(r['main']['temp']), 
        'icon' : r['weather'][0]['icon'],
        }
    context = {'city_weather': city_weather}
    return render(request, 'DublinBusTest/index.html', context)


# @csrf_protect
def load_direction(request):
    """
    Loads directions options when user selects a bus route in Search by route
    """
    if 'routeName' in request.POST:
        route = request.POST['routeName']
    else:
        route = False
    if route != False:
        direction1 = Busrouteinfojoined.objects.filter(name=route,route_direction='O',sequence_number='0')
        direction2 = Busrouteinfojoined.objects.filter(name=route,route_direction='I',sequence_number='0')
        if len(direction1) == 0:
            InboundOrigin=direction2[0].rtpi_origin
            InboundDest=direction2[0].rtpi_destination
            context = {'InboundOrigin':InboundOrigin,'InboundDest':InboundDest}
        elif len(direction2) == 0:
            OutboundOrigin=direction1[0].rtpi_origin
            OutboundDest=direction1[0].rtpi_destination
            context = { 'OutboundOrigin':OutboundOrigin,'OutboundDest':OutboundDest}
        else:    
            OutboundOrigin=direction1[0].rtpi_origin
            OutboundDest=direction1[0].rtpi_destination
            InboundOrigin=direction2[0].rtpi_origin
            InboundDest=direction2[0].rtpi_destination
            context = { 'OutboundOrigin':OutboundOrigin,'OutboundDest':OutboundDest,'InboundOrigin':InboundOrigin,'InboundDest':InboundDest}
        return render(request, 'DublinBusTest/direction_dropdown_list.html', context)

# @csrf_protect   
def load_busStops(request):
    if 'routeName' in request.POST:
        route = request.POST.get('routeName')
    else:
        route = False
    #route = request.POST.get()['routeName']
    if 'direction' in request.POST:
        direction = request.POST.get('direction')
    else:
        route = False
    stopsOnRoute = Busstopinfomerged.objects.filter(line_id=route,direction=direction).order_by('prog_no')
    context = {'stopsOnRoute': stopsOnRoute}
    return render(request, 'DublinBusTest/station_dropdown_list_options.html', context)


# @csrf_protect 

def predictNow(request):
    """
    Predicts travel time be address entry
    """
    #Initialising Lists
    Travel_times = []
    FareTotal = []
    TotalTime = []
    
    #Retrieving info from ajax call
    StartPlace=request.POST.get('startPlace')
    startId=request.POST.get('startId')
    EndPlace=request.POST.get('endPlace')
    endId=request.POST.get('endId')
    dateTime = request.POST.get('dateTime')
    departureValue = request.POST.get("value")
    timeInSeconds = request.POST.get("timeInSeconds")          

    #Making call to Google Directions API
    startLocation, endLocation, Transit, TotalTripInfo, TotalTripInfoChecker= googleDirectionsAPI(startId, endId, departureValue, timeInSeconds) 
    print(TotalTripInfo, TotalTripInfoChecker)
    
    if len(Transit)==0:
        context = {'startLocation':startLocation,'endLocation':endLocation,'startPlace':StartPlace,'endPlace':EndPlace, "Error":"Oops! This route not optimised for Dublin Bus - Try using a different mode of transport!"}
        return render(request,'DublinBusTest/predictNow.html',context ) 
    else:    
        #Check if bus stops exists in Database - if so, call model
        for i in range (0,len(Transit)):
            stopIds=Busrouteinfojoined.objects.filter(rtpi_destination=Transit[i]["destination"],name=Transit[i]["name"])
            realTime = {'route': " ",'realtime' :"Real-Time information is not available at this time"}
            if len(stopIds) <1 :
                break;
            else:
                direction = stopIds[0].route_direction
                dummies = Busstopinfomerged.objects.filter(line_id=Transit[i]["name"], direction=direction)
                #Finding Start and End stops in DB
                StartStopInfo = Busstopinfomerged.objects.filter(stop_name=Transit[i]["startLocation"], line_id=Transit[i]["name"], direction=direction)
                EndStopInfo = Busstopinfomerged.objects.filter(stop_name=Transit[i]["endLocation"], line_id=Transit[i]["name"], direction=direction)
        
                if len(StartStopInfo)==1 and len(EndStopInfo)==1:
                    #Creating stop dummies
                    stopDummies1 = [0]*len(dummies)
                    stopDummies2 = [0]*len(dummies)
                
                    #Intialising Start and End stop Ids
                    StartStop=StartStopInfo[0].stop_id
                    EndStop = EndStopInfo[0].stop_id
                           
                    for j in range (0,len(dummies)):
                        if dummies[j].stop_id == int(StartStop):
                            stopDummies1[j]=1 
                            StartStopID = stopIds[j].stop_id
                            StartStopName=stopIds[j].stop_name
                        if dummies[j].stop_id == int(EndStop):
                            stopDummies2[j]=1
                            EndStopID = stopIds[j].stop_id
                            EndStopName=stopIds[j].stop_name
                    
                     #Checking length of stop dummies
                    if direction =='I':
                        check = Directioni.objects.filter(routename=Transit[i]["name"])
                    else:
                        check = Directiono.objects.filter(routename=Transit[i]["name"])
                    for element in check:
                       extraStops = int(element.field_size)
                    extra = extraStops - len(dummies)
                    if extra > 0: 
                        extraDummies = [0]*extra
                        stopDummies1.extend(extraDummies)
                        stopDummies2.extend(extraDummies)
                    elif extra < 0: 
                            checker = stopDummies1[:extra]
                            stopDummies1 = stopDummies1[extra:]
                            checker2 = stopDummies2[:extra]
                            stopDummies2 = stopDummies2[extra:]
                            for i in range(extra):
                                if checker[i] == 1:
                                    stopDummies1[-1]=1
                                elif checker2[i] == 1:
                                    stopDummies2[-1]=1
        
                    #Calling model
                    modelcall=(Transit[i]["name"].upper())
                    result = callModel(modelcall, direction, dateTime, departureValue, stopDummies1,stopDummies2)
                    final_prediction=display_time(result)
                    realTime = getRealTime(StartStop)
                    #Changing TravelTime in Total Trip INFO to our model's prediction   
                    for i in range(len(TotalTripInfoChecker)):
                        if TotalTripInfoChecker[i]=="transit":
                            TotalTripInfo[i]["duration"] = final_prediction
                            print(final_prediction)
                    
                     #Calculate fare for journey
                    Stages1 = Busrouteinfojoined.objects.filter(route_direction=direction, name=Transit[i]["name"], id=StartStop)
                    Stages2 = Busrouteinfojoined.objects.filter(route_direction=direction, name=Transit[i]["name"], id=EndStop)
                    if len(Stages1) ==1 and len(Stages2) ==1:
                        for element in Stages1:
                            stage1 = element.stage_number
                        for element in Stages1:
                            stage2 = element.stage_number
                        if stage1==0 or stage2==0:
                            fare = "Could not calculate fare at this time."
                        else:
                            fare = calculateFare(int(stage1), int(stage2))
                    else:
                        fare = "Could not calculate fare at this time."
                    FareTotal.append(fare)
                    print(Faretotal)
                elif len(StartStopInfo)==1:
                    StartStop=StartStopInfo[0].stop_id
                    realTime = getRealTime(StartStop)
                else:
                    realTime = {'route': " ",
                            'realtime' :"Real-Time information is not available at this time"}

    #Getting total journey Time
    for i in range(len(TotalTripInfo)):
        times = TotalTripInfo[i]["duration"].split(' ')
        if len(times)!=4:
            Travel_times.append(int(times[0])*60)
        else:
            hour = (int(times[0])*60*60)
            minutes = (int(times[2])*60)
            Travel_times.append(hour+minutes)
        print(Travel_times)
        TotalTime = display_time(int(sum(Travel_times)))
   
    context={'startLocation':startLocation,'endLocation':endLocation,'startPlace':StartPlace,'endPlace':EndPlace,'TotalTime':TotalTime, "TotalTripInfo":TotalTripInfo, "Transit":Transit, 'Fare':FareTotal,'StartID':StartPlace, "realTime":realTime}
    return render(request,'DublinBusTest/predictNow.html',context )    

# @csrf_protect

def prediction(request):
    """
    Predicts Travel time by route and stop selection
    """
    #Retrieving data from ajax call
    route = request.POST.get('Route')
    direction=request.POST.get('Direction')
    StartStop=request.POST.get('StartStop')
    EndStop=request.POST.get('EndStop')
    dateTime = request.POST['dateTime']
    departureValue = request.POST.get('value')
    
    #Creating stop dummies
    stopIds=Busstopinfomerged.objects.filter(direction=direction,line_id=route)
    for i in stopIds:
        stopDummies1 = [0]*len(stopIds)
        stopDummies2 = [0]*len(stopIds)
    
        for i in range (0,len(stopIds)):
            if stopIds[i].stop_id == int(StartStop):
                stopDummies1[i]=1 
                StartStopName=stopIds[i].stop_name
                StartStopID = stopIds[i].stop_id
            if stopIds[i].stop_id == int(EndStop):
                stopDummies2[i]=1
                EndStopName=stopIds[i].stop_name
    
    #Checking length of stop dummies
    if direction =='I':
        check = Directioni.objects.filter(routename=route)
    else:
        check = Directiono.objects.filter(routename=route)
    for element in check:
       extraStops = int(element.field_size)
    extra = extraStops - len(stopIds)
    if extra > 0: 
        extraDummies = [0]*extra
        stopDummies1.extend(extraDummies)
        stopDummies2.extend(extraDummies)
    elif extra < 0: 
            checker = stopDummies1[:extra]
            stopDummies1 = stopDummies1[extra:]
            checker2 = stopDummies2[:extra]
            stopDummies2 = stopDummies2[extra:]
            for i in range(extra):
                if checker[i] == 1:
                    stopDummies1[-1]=1
                elif checker2[i] == 1:
                    stopDummies2[-1]=1
            print(len(stopDummies1))
            print(len(stopDummies2))
            
    #Calculate fare for journey
    Stages1 = Busrouteinfojoined.objects.filter(route_direction=direction, name=route, id=StartStop)
    Stages2 = Busrouteinfojoined.objects.filter(route_direction=direction, name=route, id=EndStop)
    if len(Stages1) ==1 and len(Stages2) ==1:
        for element in Stages1:
            stage1 = element.stage_number
        for element in Stages1:
            stage2 = element.stage_number
        if stage1==0 or stage2==0:
            fare = "Could not calculate fare at this time."
        else:
            fare = calculateFare(int(stage1), int(stage2))
    else:
        fare = "Could not calculate fare at this time."
         
    result = callModel(route, direction, dateTime, departureValue, stopDummies1,stopDummies2)
    final_prediction=display_time(result)
    realTime = getRealTime(StartStop)
    context={'prediction':final_prediction, 'fare':fare,"start":StartStopName, "end":EndStopName, "realTime": realTime, 'route':route, "startID":StartStopID}
    return render(request,'DublinBusTest/prediction.html',context )    

def get_routes_stops(request):
    """
    Creates an autocomplete suggestion box for user inputting line_id
    """
  # from  http://www.lalicode.com/post/5/  
    if request.is_ajax():
        q = request.GET.get('term', '')
        
        routeStopSearch = Busstopinfomerged.objects.filter(line_id__icontains=q).values_list('line_id', flat=True).distinct()
        results = []
        for stops in routeStopSearch:
            routeStopSearch.json = {}
            routeStopSearch.json = stops
            results.append(routeStopSearch.json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def leapForm(request):
    """
    returns leap card balance to user
    """
    # https://github.com/skhg/pyleapcard/blob/master/pyleapcard/PyLeapCard.py
    if 'username' in request.POST:
        username = request.POST['username']
    if 'password' in request.POST:
        password = request.POST['password']
    session = LeapSession()
    try: 
        session.try_login(username, password)
        overview = session.get_card_overview()
        returns = vars(overview)
        credit = returns['balance']
        cardnum = returns['card_num']
        cardname=returns['card_label']
        if len(returns)<=0:
            errorMessage = "Request for balance could not be processed at this time"
            context={"errorMessage":errorMessage}
        else:
            context={'credit':credit,'cardnum':cardnum,'cardname':cardname}
    except: 
        errorMessage = "Incorrect or invalid credentials. Please try again"
        context = {"errorMessage":errorMessage}
    return render(request,'DublinBusTest/leapBalance.html',context )   

def realTimeInfo(request):
    """
    Retrieving real-time stop info for user on bus stop icon click
    """
    # https://data.smartdublin.ie/dataset/c9df9a0b-d17a-40ff-a5d4-01da0cf08617/resource/4b9f2c4f-6bf5-4958-a43a-f12dab04cf61/download/rtpirestapispecification.pdf
    stopID = request.POST.get('stopId')
    stopName = request.POST.get('stopName')
    url = 'https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid={}&operator=bac&maxresults=5&format=json'
    query = urlopen(url.format(stopID)).read().decode('utf-8')
    data = json.loads(query)
    results = data["results"]
    if len(results) <= 0:
         errorHandler = "No real-time information available at this time."
         context={'stopID':stopID, 'stopName':stopName, "data":data,"errorHandler":errorHandler}
    else:
        context={'stopID':stopID, 'stopName':stopName, "data":data, "results":results}
    return render(request,'DublinBusTest/realTimeStopInfo.html',context )  

def selectedStartStationInfo(request):
    """
    Returns a list to disable stops before the start Stop
    """
    route = request.POST.get('routeName')
    direction = request.POST.get('direction')
    stops = Busstopinfomerged.objects.filter(line_id=route,direction=direction).order_by("prog_no")
    results = []
    for stop in stops:
        results.append(stop.stop_id)
    return HttpResponse(json.dumps(results), content_type="application/json")

def selectedEndStationInfo(request):
    """
    Returns a list to disable stops after the end Stop
    """
    route = request.POST.get('routeName')
    direction = request.POST.get('direction')
    stops = Busstopinfomerged.objects.filter(line_id=route,direction=direction).order_by("prog_no")
    results = []
    for stop in stops:
        results.append(stop.stop_id)
    return HttpResponse(json.dumps(results), content_type="application/json")