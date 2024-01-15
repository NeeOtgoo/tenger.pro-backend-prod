from django.db.models import CharField, ForeignKey, CASCADE, Model
from apps.school.models import School

class Sub_school(Model):
    name = CharField(max_length=250)
    name_mgl = CharField(max_length=250)
    school = ForeignKey(School, on_delete=CASCADE)

    def __str__(self):
        return 'id: '+str(self.pk)+' | name: '+self.name
