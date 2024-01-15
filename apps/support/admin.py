from django.contrib import admin
from .models import Support, SupportFile, SupportGroup

# Register your models here.
admin.site.register(Support)
admin.site.register(SupportFile)
admin.site.register(SupportGroup)
