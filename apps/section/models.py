from django.db.models import CharField, ForeignKey, DateTimeField, IntegerField, CASCADE, Model
from django.conf import settings
from apps.sub_school.models import Sub_school
from apps.school.models import School
from apps.program.models import Program
from apps.classes.models import Classes

class Section(Model):
    section = CharField(max_length=150)
    classes = ForeignKey(Classes, on_delete=CASCADE)
    program = ForeignKey(Program, on_delete=CASCADE)
    sub_school = ForeignKey(Sub_school, on_delete=CASCADE)
    school = ForeignKey(School, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def __str__(self):
        return 'id: '+str(self.pk)+' | section: '+self.section+' | classes: ('+str(self.classes)+') | program: ('+str(self.program)+')'
