from django.urls import path
from DublinBusTest import views



# Code below routes the different aspects of the webpage to the required URL
urlpatterns = [
    path('', views.index, name='index'),
    path('prediction/', views.prediction, name='prediction'),
    path('load_direction/', views.load_direction, name='load_direction'),
    path('load_busStops/', views.load_busStops, name='load_busStops'),
    path('predictNow/', views.predictNow, name='predictNow'),
    path('leapForm/', views.leapForm, name='leapForm'),
    path('realTimeInfo/', views.realTimeInfo, name='realTimeInfo'),
     path('selectedStartStationInfo/', views.selectedStartStationInfo, name='selectedStartStationInfo'),
    path('selectedEndStationInfo/', views.selectedEndStationInfo, name='selectedEndStationInfo'),
    path('api/get_routes_stops/', views.get_routes_stops, name='get_routes_stops'),

]
