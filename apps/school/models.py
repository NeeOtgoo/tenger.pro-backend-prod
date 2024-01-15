from django.db.models import CharField, TextField, Model, FloatField

class School(Model):
    name = CharField(max_length=50)
    name_mgl = CharField(max_length=50)
    report_text = TextField()

    def __str__(self):
        return 'id: '+str(self.pk)+' | '+self.name

class School_location(Model):
    lon = FloatField()
    lat = FloatField()
