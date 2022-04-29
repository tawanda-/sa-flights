from django.contrib import admin
from .models import Aircraft, Airport, Flight, AirportAdmin, FlightAdmin

admin.site.register(Airport, AirportAdmin)
admin.site.register(Aircraft)
admin.site.register(Flight, FlightAdmin)