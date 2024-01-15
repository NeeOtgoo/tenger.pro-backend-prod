from django.db.models import Model, CharField, DateTimeField, IntegerField, ForeignKey, TextField, CASCADE
from apps.teacher.models import Teacher
from django.conf import settings
from apps.section.models import Section

# Create your models here.
class Live(Model):
    STATUS_CHOICES = (
        ('OPEN', 'Нээлттэй',),
        ('CLOSED', 'Хаалттай',),
    )
    TYPE_CHOICES = (
        ('WEBINAR', 'Вебинар',),
        ('ZOOM', 'Хурал',),
    )
    title = CharField(max_length=250)
    date = DateTimeField()
    duration = IntegerField(blank=False)
    description = TextField(blank=True)
    status = CharField(
        max_length=10,
        choices=STATUS_CHOICES,
    )
    type = CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='WEBINAR'
    )
    teacher = ForeignKey(Teacher, on_delete=CASCADE)
    section = ForeignKey(Section, on_delete=CASCADE)
    meeting_id = TextField(blank=True)
    password = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def filter_fields():
        return ['title']

class Live_config(Model):
    client_id = CharField(blank=True,max_length=765)
    client_secret = CharField(blank=True,max_length=765)
    api_key = CharField(blank=True,max_length=765)
    api_secret = CharField(blank=True,max_length=765)
    data = TextField(blank=True)