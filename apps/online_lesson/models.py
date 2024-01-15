from django.db.models import Model, CharField, DateTimeField, IntegerField, ForeignKey, TextField, FileField, ManyToManyField, CASCADE
from django.conf import settings
from apps.subject.models import Subject
from apps.student.models import Student
from apps.schoolyear.models import Schoolyear
from tenants.middlewares import get_current_db_name

# Create your models here.
class Online_lesson(Model):
    STATUS_CHOICES = (
        ('OPEN', 'Нээлттэй',),
        ('CLOSED', 'Хаалттай',),
    )
    schoolyear = ForeignKey(Schoolyear, on_delete=CASCADE)
    subject = ForeignKey(Subject, on_delete=CASCADE)
    description = TextField(blank=True)
    content = TextField(blank=True)
    status = CharField(
        max_length=10,
        choices=STATUS_CHOICES,
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def filter_fields():
        return ['subject__subject','description','content']

class Online_student(Model):
    online_lesson = ForeignKey(Online_lesson, on_delete=CASCADE)
    student = ForeignKey(Student, on_delete=CASCADE)

class Online_file_folder(Model):
    name = CharField(max_length=200)
    sub_folder = ForeignKey("self", on_delete=CASCADE, blank=True, null=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, blank=True, null=True)

class Online_file(Model):
    upload_path = 'default'
    if(get_current_db_name()!=None):
        upload_path = get_current_db_name()
    file =FileField(upload_to='static/uploads/'+upload_path+'/online_lessons/%Y/%m/%d/', max_length=500)
    folder = ForeignKey(Online_file_folder, on_delete=CASCADE, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

class Online_type(Model):
    name = CharField(max_length=120)

class Online_sub(Model):
    STATUS_CHOICES = (
        ('OPEN', 'Нээлттэй',),
        ('CLOSED', 'Хаалттай',),
    )
    title = CharField(max_length=120)
    description = TextField(blank=True)
    content = TextField(blank=True)
    online_lesson = ForeignKey(Online_lesson, on_delete=CASCADE)
    online_type = ForeignKey(Online_type, on_delete=CASCADE)
    status = CharField(
        max_length=10,
        choices=STATUS_CHOICES,
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

class Online_attendance(Model):
    online_sub = ForeignKey(Online_sub, on_delete=CASCADE)
    student = ForeignKey(Student, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

class Online_sub_file(Model):
    online_sub = ForeignKey(Online_sub, on_delete=CASCADE)
    online_file = ForeignKey(Online_file, on_delete=CASCADE)
