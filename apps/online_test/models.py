from django.db.models import CharField,  ForeignKey, TextField, DateTimeField, IntegerField, ImageField, DecimalField,  Model, CASCADE, SET_NULL
from apps.subject.models import Subject
from apps.student.models import Student
from django.conf import settings
from tenants.middlewares import get_current_db_name

class Online_test(Model):
    title = CharField(max_length=50)
    description = TextField(max_length=500)
    subject = ForeignKey(Subject, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, related_name = 'online_test_create_userID', on_delete=CASCADE)

class Question_level(Model):
    level = CharField(max_length=500)

class Question(Model):
    upload_path = 'default'
    if(get_current_db_name()!=None):
        upload_path = get_current_db_name()
    ATYPE_CHOICES = (
        ('CHOOSE', 'Нэг сонголт',),
        ('MULTIPLE', 'Олон сонголт',),
        ('TEXT', 'Бичвэр',),
    )
    online_test = ForeignKey(Online_test, on_delete=CASCADE)
    question_level = ForeignKey(Question_level, on_delete=CASCADE, blank=True, null=True)
    question = TextField(max_length=500, blank=False)
    hint = TextField(max_length=500, blank=True, null=True)
    image = ImageField(upload_to='static/uploads/'+upload_path+'/online_test/%Y/%m/%d/', blank=True, null=True)
    answer_type = CharField(
        max_length=10,
        choices=ATYPE_CHOICES,
    )

class Question_choice(Model):
    question = ForeignKey(Question, on_delete=CASCADE)
    answer = TextField(max_length=500)
    score = DecimalField(max_digits=12, decimal_places=2, default=0)

class Take_test(Model):
    STATUS_CHOICES = (
        ('OPEN', 'Нээлттэй',),
        ('CLOSED', 'Хаалттай',),
    )
    title = CharField(max_length=50)
    description = TextField(max_length=500)
    start_at = DateTimeField(blank=False)
    end_at = DateTimeField(blank=False)
    duration = IntegerField(blank=False, default=0)
    status = CharField(
        max_length=10,
        choices=STATUS_CHOICES,
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, related_name = 'take_test_create_userID', on_delete=CASCADE)

class Take_level(Model):
    take_test = ForeignKey(Take_test, on_delete=CASCADE)
    online_test = ForeignKey(Online_test, on_delete=CASCADE)
    question_level = ForeignKey(Question_level, on_delete=CASCADE)
    take_number = IntegerField(blank=False, default=0)

class Participant(Model):
    student = ForeignKey(Student, on_delete=CASCADE)
    take_test = ForeignKey(Take_test, on_delete=CASCADE)
    started = DateTimeField(blank=True, null=True)
    completed = DateTimeField(blank=True, null=True)

class Answer(Model):
    ATYPE_CHOICES = (
        ('CHOOSE', 'Нэг сонголт',),
        ('MULTIPLE', 'Олон сонголт',),
        ('TEXT', 'Бичвэр',),
    )
    participant = ForeignKey(Participant, on_delete=CASCADE)
    question = ForeignKey(Question, on_delete=SET_NULL, null=True)
    question_text = TextField(max_length=500, blank=False)
    choices = TextField(max_length=2500, blank=False, default="")
    answer_type = CharField(
        max_length=10,
        choices=ATYPE_CHOICES,
        default="CHOOSE"
    )
    given_answer = TextField(max_length=500, default="")
    score = DecimalField(max_digits=12, decimal_places=2, default=0)
    timestamp = DateTimeField(auto_now=True)