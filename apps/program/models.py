from django.db.models import CharField, ForeignKey, DateTimeField, IntegerField, TextField, CASCADE, Model
from django.conf import settings
from apps.sub_school.models import Sub_school
from apps.school.models import School
from apps.core.models import Degree
from apps.subject.models import Subject
from django.contrib.auth import get_user_model

class Program(Model):
    STATUS_CHOICES = (
        ('OPEN', 'Нээлттэй',),
        ('CLOSED', 'Хаалттай',),
    )
    program = CharField(max_length=250)
    program_mgl = CharField(max_length=250)
    program_numeric = CharField(max_length=50)
    degree = ForeignKey(Degree, on_delete=CASCADE)
    max_student_num = IntegerField()
    school = ForeignKey(School, on_delete=CASCADE)
    sub_school = ForeignKey(Sub_school, on_delete=CASCADE)
    status = CharField(
        max_length=10,
        choices=STATUS_CHOICES,
    )
    report_text = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def __str__(self):
        return 'id: '+str(self.pk)+' | program: '+self.program

    def access_program(teacher):
        if teacher.access == 'A_1':
            return Program.objects.all().values('id')
        elif teacher.access == 'A_2':
            return Program.objects.filter(school=teacher.school).values('id')
        elif teacher.access == 'A_3':
            return Program.objects.filter(sub_school=teacher.sub_school).values('id')
        elif teacher.access == 'A_4':
            user_i = get_user_model().objects.get(pk=teacher.user_id)
            return Program.objects.filter(create_userID=user_i).values('id')

class Program_subject(Model):
    program = ForeignKey(Program, on_delete=CASCADE)
    subject = ForeignKey(Subject, on_delete=CASCADE)