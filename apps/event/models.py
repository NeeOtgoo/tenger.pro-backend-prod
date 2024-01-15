from django.db.models import CharField, ForeignKey, DateTimeField, TextField, CASCADE, Model
from django.conf import settings

class Event_type(Model):
    name = CharField(max_length=50)
    color = CharField(max_length=50)

    def __str__(self):
        return self.name

class Event(Model):
    title = CharField(max_length=50)
    description = TextField(max_length=500)
    content = TextField()
    start_at = DateTimeField()
    end_at = DateTimeField()
    event_type = ForeignKey(Event_type, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, related_name = 'event_create_userID', on_delete=CASCADE)

    def __str__(self):
        return self.title

