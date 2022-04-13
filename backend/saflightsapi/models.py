from django.db import models

# airport details
class Airport(models.Model):
    icao_code = models.CharField(max_length=25, primary_key = True)
    iata_code = models.CharField(max_length=25)
    name = models.CharField(max_length=250)
    municipality = models.CharField(max_length=250)
    latitude_deg = models.FloatField(blank=True, null=True)
    longitude_deg = models.FloatField(blank=True, null=True)
    elevation = models.IntegerField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name 

class FlightDetail(models.Model):

    class Meta:
       ordering = ['time_scheduled']

    STATUS_CHOICE = [
        ('DEPARTURE', 'departure'),
        ('ARRIVAL', 'arrival'),
    ]
    status = models.CharField(max_length=10,choices=STATUS_CHOICE)
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
        return '%s %s' % (self.time_scheduled, self.status)

class Flight(models.Model):

    number = models.CharField(max_length=20, blank=True, null=True)
    iata_code = models.CharField(max_length=20, blank=True, null=True)
    icao_code = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=False, blank=False) #icao/iata code
    source_airport = models.ForeignKey('Airport', related_name='departure_airport_set',on_delete=models.CASCADE)
    destination_airport = models.ForeignKey('Airport', related_name='arrival_airport_set',on_delete=models.CASCADE)
    status = models.CharField(max_length=20, blank=True, null=True)
    airline = models.CharField(max_length=250, blank=True, null=True)
    departure = models.ForeignKey('FlightDetail', related_name='departure_flight_set',on_delete=models.CASCADE)
    arrival = models.ForeignKey('FlightDetail', related_name='arrival_flight_set', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.airline