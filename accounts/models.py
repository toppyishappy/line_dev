from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from line.line_class import Line
class User(AbstractUser):

    CUSTOMER = 'customer'
    BOOKER = 'booker'

    ROLE_CHOICES = (
        (CUSTOMER, 'customer'),
        (BOOKER, 'booker'),
    )

    phone_number    = models.CharField(max_length=20, blank=True)
    line            = models.CharField(max_length=20, blank=True)
    role            = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)
    
    def get_user_info_line(self, user_id):
        url = 'https://api.line.me/v2/bot/profile/' + user_id
        headers = {
            'Authorization': f'Bearer {settings.CHANNEL_ACCESS_TOKEN}'
        }
        print('headers', headers)
        instance = Line()
        response = instance.http_request(method='GET', url=url, headers=headers)
        if response:
            self.username = response['displayName']
            self.user_id = response['userId']
            self.profile_url = response['pictureUrl']
            self.save()