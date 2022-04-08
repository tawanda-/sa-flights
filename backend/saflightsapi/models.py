from django.db import models

# airport details
class Airport(models.Model):
    iata_code = models.CharField(max_length=25, primary_key = True)
    name = models.CharField(max_length=250)
    municipality = models.CharField(max_length=250)
    latitude_deg = models.FloatField(blank=True, null=True)
    longitude_deg = models.FloatField(blank=True, null=True)
    elevation = models.IntegerField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.airport_name 

class Flight(models.Model):
    number = models.CharField(max_length=20)
    date = models.DateField(null=False, blank=False)
    status = models.CharField(max_length=20, blank=True)
    airline = models.CharField(max_length=250, blank=True)
    
    def __str__(self):
        return self.number

class FlightDetail(models.Model):

    STATUS_CHOICE = [
        ('DEPARTURE', 'departure'),
        ('ARRIVAL', 'arrival'),
    ]

    number = models.CharField(max_length=20)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICE
    )
    airport = models.CharField(max_length=250)
    iata = models.CharField(max_length=10)
    icao = models.CharField(max_length=10)
    terminal = models.CharField(max_length=250)
    gate = models.CharField(max_length=250)
    baggage = models.CharField(max_length=250)
    time_delay = models.TimeField(blank=True, null=True)
    time_scheduled = models.TimeField(blank=True, null=True)
    time_estimated = models.TimeField(blank=True, null=True)
    time_actual = models.TimeField(blank=True, null=True)
    estimated_runway = models.CharField(max_length=250, blank=True, null=True)
    actual_runway = models.CharField(max_length=250, blank=True, null=True)
    
    def __str__(self):
        return self.flight_number