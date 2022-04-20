from django.contrib import admin
from .models import Airport, Arrival, Departure, Flight

admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Departure)
admin.site.register(Arrival)
