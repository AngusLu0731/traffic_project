from django.contrib import admin

from .models import Stream, parking, speedLot, towing

# Register your models here.
admin.site.register(Stream)
admin.site.register(parking)
admin.site.register(speedLot)
admin.site.register(towing)