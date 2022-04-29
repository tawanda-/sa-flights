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

class Flight(models.Model):

    number = models.CharField(max_length=20, blank=True, null=True)
    iata_code = models.CharField(max_length=20, blank=True, null=True)
    icao_code = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=False, blank=False) 
    status = models.CharField(max_length=20, blank=True, null=True)
    airline = models.CharField(max_length=250, blank=True, null=True)

    departure_airport = models.ForeignKey('Airport', related_name='departurex',on_delete=models.CASCADE)
    departure_terminal = models.CharField(max_length=250, blank=True, null=True)
    departure_gate = models.CharField(max_length=250, blank=True, null=True)
    departure_baggage = models.CharField(max_length=250, blank=True, null=True)
    departure_time_delay = models.IntegerField(blank=True, null=True)
    departure_time_scheduled = models.TimeField(blank=True, null=True)
    departure_time_actual = models.TimeField(blank=True, null=True)

    arrival_airport = models.ForeignKey('Airport', related_name='arrivalx',on_delete=models.CASCADE)
    arrival_terminal = models.CharField(max_length=250, blank=True, null=True)
    arrival_gate = models.CharField(max_length=250, blank=True, null=True)
    arrival_baggage = models.CharField(max_length=250, blank=True, null=True)
    arrival_time_delay = models.IntegerField(blank=True, null=True)
    arrival_time_scheduled = models.TimeField(blank=True, null=True)
    arrival_time_actual = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.number}, {self.airline}"

class AirportAdmin(admin.ModelAdmin):
    search_fields = ["icao_code", "iata_code", "city", "country", "name"]

class FlightAdmin(admin.ModelAdmin):
    search_fields = ["icao_code", "iata_code", "number", "airline", "departure__time_scheduled"]