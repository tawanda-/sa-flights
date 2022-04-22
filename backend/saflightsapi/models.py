from django.contrib import admin
from django.db import models

class Airport(models.Model):

    class Meta:
       ordering = ['name']

    icao_code = models.CharField(max_length=25, blank=True, null=True)
    iata_code = models.CharField(max_length=25, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    latitude_deg = models.FloatField(blank=True, null=True)
    longitude_deg = models.FloatField(blank=True, null=True)
    elevation = models.IntegerField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return '%s %s' % (self.name, self.icao_code)

class Aircraft(models.Model):

    category = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    icao = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self) -> str:
        return self.type

class Departure(models.Model):

    class Meta:
       ordering = ['time_scheduled']

    airport = models.ForeignKey('Airport', on_delete=models.CASCADE)
    terminal = models.CharField(max_length=250, blank=True, null=True)
    gate = models.CharField(max_length=250, blank=True, null=True)
    baggage = models.CharField(max_length=250, blank=True, null=True)
    time_delay = models.IntegerField(blank=True, null=True)
    time_scheduled = models.TimeField(blank=True, null=True)
    time_estimated = models.TimeField(blank=True, null=True)
    time_actual = models.TimeField(blank=True, null=True)
    estimated_runway = models.CharField(max_length=250, blank=True, null=True)
    actual_runway = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.time_scheduled, self.airport)

class Arrival(models.Model):

    class Meta:
       ordering = ['time_scheduled']

    airport = models.ForeignKey('Airport', on_delete=models.CASCADE)
    terminal = models.CharField(max_length=250, blank=True, null=True)
    gate = models.CharField(max_length=250, blank=True, null=True)
    baggage = models.CharField(max_length=250, blank=True, null=True)
    time_delay = models.IntegerField(blank=True, null=True)
    time_scheduled = models.TimeField(blank=True, null=True)
    time_estimated = models.TimeField(blank=True, null=True)
    time_actual = models.TimeField(blank=True, null=True)
    estimated_runway = models.CharField(max_length=250, blank=True, null=True)
    actual_runway = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.time_scheduled, self.airport)

class Flight(models.Model):

    number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    iata_code = models.CharField(max_length=20, blank=True, null=True)
    icao_code = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=False, blank=False) 
    status = models.CharField(max_length=20, blank=True, null=True)
    airline = models.CharField(max_length=250, blank=True, null=True)
    departure = models.ForeignKey('Departure', on_delete=models.CASCADE)
    arrival = models.ForeignKey('Arrival', on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s %s' % (self.number, self.airline, self.departure, self.arrival)

class AirportAdmin(admin.ModelAdmin):
    search_fields = ["icao_code", "iata_code", "city", "country", "name"]

class FlightAdmin(admin.ModelAdmin):
    search_fields = ["icao_code", "iata_code", "number", "airline", "departure__time_scheduled"]

class ArrivalAdmin(admin.ModelAdmin):
    search_fields = ["airport__name", "airport__icao_code", "airport__iata_code"]

class DepartureAdmin(admin.ModelAdmin):
    search_fields = ["airport__name", "airport__icao_code", "airport__iata_code"]