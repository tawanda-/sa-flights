from django.db import models

class Flight(models.Model):
    number = models.CharField(max_length=20)
    date = models.DateField(null=False, blank=False)
    status = models.CharField(max_length=20, blank=True)
    airline = models.CharField(max_length=250, blank=True)
    
    def __str__(self):
        return self.number
