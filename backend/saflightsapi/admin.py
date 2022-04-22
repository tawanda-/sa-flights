from django.contrib import admin
from .models import Aircraft, Airport, Arrival, ArrivalAdmin, Departure, DepartureAdmin, Flight, AirportAdmin, FlightAdmin

admin.site.register(Airport, AirportAdmin)
admin.site.register(Aircraft)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Departure, DepartureAdmin)
admin.site.register(Arrival, ArrivalAdmin)