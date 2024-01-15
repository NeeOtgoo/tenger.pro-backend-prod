from django.db.models import Model, CharField, DateField, DateTimeField, ForeignKey, TextField, FileField, ManyToManyField, CASCADE
from django.conf import settings
from django.db.models.fields import IntegerField
from graphene.types.scalars import Int
from apps.program.models import Program
from apps.classes.models import Classes
from apps.section.models import Section
from apps.subject.models import Subject
from apps.student.models import Student
from apps.teacher.models import Teacher
from apps.schoolyear.models import Schoolyear

# Create your models here.

class Routine(Model):
    schoolyear = ForeignKey(Schoolyear, on_delete=CASCADE)
    program = ForeignKey(Program, on_delete=CASCADE)
    classes = ForeignKey(Classes, on_delete=CASCADE)
    section = ForeignKey(Section, on_delete=CASCADE)
    subject = ForeignKey(Subject, on_delete=CASCADE)
    teacher = ForeignKey(Teacher, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    
    def filter_fields():
        return ['teacher__family_name','teacher__name','program__program','classes__classes',]


class Routine_student(Model):
    routine = ForeignKey(Routine, on_delete=CASCADE)
    student = ForeignKey(Student, on_delete=CASCADE)

class Routine_time(Model):
    routine = ForeignKey(Routine, on_delete=CASCADE)
    type = CharField(blank=False, max_length=100)
    time = IntegerField(default=1)
    date = DateField(blank=False)
    room = CharField(max_length=50, blank=False)
    
    def __str__(self):
        return 'id: '+str(self.pk)+' | routine: '+str(self.routine)+' | type: '+str(self.type)+' | time: '+str(self.time)+' | date: '+str(self.date)+' | room: '+str(self.room)

        
    def filter_fields():
        return ['type',]

class Routine_attendance(Model):
    STATUS_CHOICES = (
        ('ARRIVED', 'Ирсэн',),
        ('INTERRUPTED', 'Тасалсан',),
        ('SICK', 'Өвчтэй',),
        ('FREE', 'Чөлөөтэй',),
    )
    student = ForeignKey(Student, on_delete=CASCADE)
    routine_time = ForeignKey(Routine_time, on_delete=CASCADE)
    point = CharField(max_length=10)
    status = CharField(
        max_length=20,
        choices=STATUS_CHOICES,
    )