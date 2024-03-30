from django.contrib import admin
from car_auction.models import (CustomUser, Cars)

admin.site.register(CustomUser)
admin.site.register(Cars)

# Register your models here.
