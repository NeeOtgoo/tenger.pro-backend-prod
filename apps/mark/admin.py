from django.contrib import admin
from .models import Mark_board, Mark, Mark_percentage, Mark_rel, Mark_setting

# Register your models here.
admin.site.register(Mark_board)
admin.site.register(Mark)
admin.site.register(Mark_percentage)
admin.site.register(Mark_rel)
admin.site.register(Mark_setting)
