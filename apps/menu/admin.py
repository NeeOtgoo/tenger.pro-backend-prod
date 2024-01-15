from django.contrib import admin
from .models import Menu

# Register your models here.
# class MenuAdmin(admin.ModelAdmin):
#     # a list of displayed columns name.
#     list_display = ['id', 'title', 'key', 'path']
# admin.site.register(MenuAdmin)
admin.site.register(Menu)