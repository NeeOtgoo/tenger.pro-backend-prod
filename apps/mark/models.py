from django.db.models import Model, CharField, DateTimeField, IntegerField, ForeignKey, DecimalField, IntegerChoices, CASCADE
from django.conf import settings
from apps.schoolyear.models import Schoolyear
from apps.subject.models import Subject
from apps.student.models import Student
from apps.teacher.models import Teacher

class Mark_board(Model):
    STATUS_CHOICES = (
        ('OPEN', 'Нээлттэй',),
        ('CLOSED', 'Хаалттай',),
    )
    schoolyear = ForeignKey(Schoolyear, on_delete=CASCADE)
    subject = ForeignKey(Subject, on_delete=CASCADE)
    teacher = ForeignKey(Teacher, on_delete=CASCADE)
    start_at = DateTimeField()
    end_at = DateTimeField()
    status = CharField(
        max_length=10,
        choices=STATUS_CHOICES,
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def filter_fields():
        return ['subject__subject','teacher__teacher_code','teacher__family_name','teacher__name']

class Mark(Model):
    mark_board = ForeignKey(Mark_board, on_delete=CASCADE)
    student = ForeignKey(Student, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

class Mark_percentage(Model):
    type = CharField(max_length=120)
    percentage = IntegerField()
    diam = DecimalField(max_digits=5, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def __str__(self):
        return 'type: '+self.type+' | percentage: '+str(self.percentage)+' | diam: '+str(self.diam)

class Mark_setting(Model):
    PART_CHOICES = (
        ('A', 'Ерөнхий суурь хэсэг',),
        ('B', 'Техникийн /Мэргэжлийн/ суурь хэсэг',),
        ('C', 'Мэргэшүүлэх хэсэг',),
    )
    name = CharField(max_length=120)
    percentage = IntegerField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    pass_val = IntegerField(default=60)
    part = CharField(
        max_length=5,
        choices=PART_CHOICES,
        default='A'
    )
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def __str__(self):
        return 'name: '+self.name+' | percentage: '+str(self.percentage)

class Mark_rel(Model):
    mark = ForeignKey(Mark, on_delete=CASCADE)
    mark_setting = ForeignKey(Mark_setting, on_delete=CASCADE)
    mark_val = DecimalField(max_digits=5, decimal_places=2)
  