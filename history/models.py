from django.db import models

class ReservartionHistory(models.Model):
    user            = models.CharField(max_length=10) # {pk user}
    user_name       = models.CharField(max_length=20) 
    location        = models.TextField(default="", null=True) # {lat: 00 , lng: 00}
    reserved_date   = models.DateTimeField(null=True)
    is_paid         = models.BooleanField(default=False)
    is_cancled      = models.BooleanField(default=False)
    booker          = models.CharField(max_length=10, blank=True, null=True)  # {pk booker}

    created_on      = models.DateTimeField(auto_now_add=True)
    updated_on      = models.DateTimeField(auto_now=True)
