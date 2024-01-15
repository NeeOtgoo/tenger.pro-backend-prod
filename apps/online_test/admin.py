from django.contrib import admin
from .models import Online_test, Question_level, Question, Question_choice, Take_test, Take_level, Participant, Answer

# Register your models here.
admin.site.register(Online_test)
admin.site.register(Question_level)
admin.site.register(Question)
admin.site.register(Question_choice)
admin.site.register(Take_test)
admin.site.register(Take_level)
admin.site.register(Participant)
admin.site.register(Answer)