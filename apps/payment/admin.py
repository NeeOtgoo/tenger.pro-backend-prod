from django.contrib import admin
from .models import Payment, Invoice, Invoice_stock

# Register your models here.
admin.site.register(Payment)
admin.site.register(Invoice)
admin.site.register(Invoice_stock)