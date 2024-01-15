from django.db.models import Model, CharField, ForeignKey, CASCADE, IntegerField, TextField
from ..teacher.models import Teacher
from ..subject.models import Subject
from ..section.models import Section
from ..schoolyear.models import Schoolyear
from ..employee.models import Employee

# Create your models here.

class PlanMark(Model):
    name = CharField(max_length=100)

class Plan(Model):
    title = CharField(max_length=50)
    teacher = ForeignKey(Teacher, on_delete=CASCADE)
    subject = ForeignKey(Subject, on_delete=CASCADE)
    section = ForeignKey(Section, on_delete=CASCADE)
    schoolyear = ForeignKey(Schoolyear, on_delete=CASCADE)
    approved_by = ForeignKey(Employee, on_delete=CASCADE, blank=True, null=True)
    #Бүлэг сэдэв
    topic = CharField(max_length=50)
    #Ээлжит хичээлийн сэдэв
    subject_topic = CharField(max_length=50)
    #Суралцахуйн зорилт
    intention = TextField(blank=True)
    #Түлхүүр үг
    keyword = CharField(max_length=100)
    #Хэрэглэгдэхүүн
    consumables = TextField(blank=True)
    duration = IntegerField()

    class Meta:
        permissions = [
            ("approve_plan", "Can approve plan"),
        ]
class PlanAction(Model):
    plan = ForeignKey(Plan, on_delete=CASCADE)
    plan_mark = TextField(blank=True)
    name = CharField(max_length=50)
    teaching_method = CharField(max_length=100)
    teacher_activity = TextField(blank=True)
    student_activity = TextField(blank=True)
    student_assignment = TextField(blank=True)
    duration = IntegerField()
