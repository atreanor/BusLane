from django.db import models
from django.shortcuts import render

class StopStaticInfo(models.Model):

    """Corresponds to the data in the StopStaticInfo Model
    Created using python manage.py inspectdb - gives you the model classes that can be used here"""

    number = models.IntegerField()
    stop_name = models.CharField(max_length=100)
    stop_lat = models.FloatField()
    stop_lon = models.FloatField()
    stop_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'Stop_Static_Info'

# class Busrouteinfo(models.Model):
#     id = models.BigIntegerField(db_column='ID', primary_key=True)
#     location_text = models.CharField(db_column='LOCATION_TEXT', max_length=60, blank=True, null=True)
#     address = models.CharField(db_column='ADDRESS', max_length=60, blank=True, null=True)
#     status = models.CharField(db_column='STATUS', max_length=15, blank=True, null=True)
#     name = models.CharField(db_column='NAME', max_length=5, primary_key=True)
#     route_direction = models.CharField(db_column='ROUTE_DIRECTION', primary_key=True, max_length=2)
#     is_stage_point = models.CharField(db_column='IS_STAGE_POINT', max_length=2, blank=True, null=True)
#     stage_number = models.CharField(db_column='STAGE_NUMBER',max_length=4, blank=True, null=True)
#     rtpi_destination = models.CharField(db_column='RTPI_DESTINATION', max_length=60, blank=True, null=True)
#     rtpi_orgin = models.CharField(db_column='RTPI_ORGIN', max_length=60, blank=True, null=True)
#     sequence_number = models.BigIntegerField(db_column='SEQUENCE_NUMBER', blank=True, null=True)
# 
#     class Meta:
#         managed = False
#         db_table = 'BusRouteInfo' 

class Busrouteinfojoined(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    location_text = models.CharField(db_column='LOCATION_TEXT', max_length=100)  # Field name made lowercase.
    address = models.CharField(db_column='ADDRESS', max_length=45, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=45, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', primary_key=True, max_length=45)  # Field name made lowercase.
    route_direction = models.CharField(db_column='ROUTE_DIRECTION', primary_key=True, max_length=45)  # Field name made lowercase.
    is_stage_point = models.CharField(db_column='IS_STAGE_POINT', max_length=45, blank=True, null=True)  # Field name made lowercase.
    stage_number = models.CharField(db_column='STAGE_NUMBER', max_length=45, blank=True, null=True)  # Field name made lowercase.
    rtpi_destination = models.CharField(db_column='RTPI_DESTINATION', max_length=45, blank=True, null=True)  # Field name made lowercase.
    rtpi_origin = models.CharField(db_column='RTPI_ORIGIN', max_length=45, blank=True, null=True)  # Field name made lowercase.
    sequence_number = models.IntegerField(db_column='SEQUENCE_NUMBER', blank=True, null=True)  # Field name made lowercase.
    number = models.IntegerField()
    stop_name = models.CharField(max_length=100)
    stop_lat = models.CharField(max_length=45)
    stop_lon = models.CharField(max_length=45)
    stop_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'BusRouteInfoJoined'
        unique_together = (('id', 'name', 'route_direction'),)
        
class Routes(models.Model):
    route_id = models.IntegerField(primary_key=True)
    route_short_name = models.CharField(db_column='route_short_name',max_length=45, blank=True, null=True)
    route_order_col = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'routes'

class Weatherforecast(models.Model):
    dt_txt = models.TextField(primary_key=True)
    temp = models.FloatField(blank=True, null=True)
    wind_speed = models.FloatField(blank=True, null=True)
    main = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'WeatherForecast'

class Busstopinfomerged(models.Model):
    stop_id = models.IntegerField()
    stop_lat = models.FloatField(blank=True, null=True)
    stop_lon = models.FloatField(blank=True, null=True)
    stop_name = models.CharField(max_length=100)
    direction = models.CharField(primary_key=True, max_length=2)
    line_id = models.CharField(max_length=5)
    prog_no = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BusStopInfoMerged'
        unique_together = (('direction', 'line_id', 'stop_id'),)
        
class Directioni(models.Model):
    routename = models.CharField(db_column='RouteName', primary_key=True, max_length=5)  # Field name made lowercase.
    field_size = models.IntegerField(db_column=' Size')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'DirectionI'


class Directiono(models.Model):
    routename = models.CharField(db_column='RouteName', primary_key=True, max_length=5)  # Field name made lowercase.
    field_size = models.IntegerField(db_column=' Size', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'DirectionO'
