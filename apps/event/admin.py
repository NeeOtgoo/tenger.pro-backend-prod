from django.contrib import admin
from .models import Event_type, Event

# Register your models here.
admin.site.register(Event_type)
admin.site.register(Event)
