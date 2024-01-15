from email.policy import default
from django.db.models import Model, CharField, DateField, DateTimeField, IntegerField, ForeignKey, DecimalField, CASCADE
from django.conf import settings
# from apps.schoolyear.models import Schoolyear
from apps.school.models import School
from apps.sub_school.models import Sub_school

# Create your models here.
class Subject(Model):
    PART_CHOICES = (
        ('A', 'Мэргэшүүлэх',),
        ('B', 'Тусгай',),
        ('C', 'Мэргэшүүлэх хэсэг',),
    )
    school = ForeignKey(School, on_delete=CASCADE)
    sub_school = ForeignKey(Sub_school, on_delete=CASCADE)
    subject = CharField(max_length=200)
    subject_mgl = CharField(max_length=200)
    subject_eng = CharField(max_length=200, default='')
    subject_code = CharField(max_length=50)
    credit = DecimalField(max_digits=200, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    part = CharField(
        max_length=50,
        choices=PART_CHOICES,
        default='A'
    )

    def __str__(self):
        return self.subject

    def filter_fields():
        return ['school__name','subject','subject_mgl','subject_code','credit']
