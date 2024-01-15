from django.db.models import TextField, CharField, ForeignKey, FileField, DateTimeField, CASCADE, Model
from django.conf import settings
from apps.student.models import Student
from tenants.middlewares import get_current_db_name

class Diplom(Model):
    name = CharField(max_length=100)
    main_mid = TextField()
    main_bottom1 = TextField()
    main_bottom2 = TextField()
    main_bottom3 = TextField()
    mgl_main_mid = TextField()
    mgl_main_bottom1 = TextField()
    mgl_main_bottom2 = TextField()
    mgl_main_bottom3 = TextField()
    mgl_main_bottom1_sub = TextField()
    mgl_main_bottom2_sub = TextField()
    mgl_main_bottom3_sub = TextField()
    mark_bottom1 = TextField()
    mark_bottom2 = TextField()
    mgl_mark_bottom1 = TextField()
    mgl_mark_bottom2 = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

class Diplom_archive(Model):
    upload_path = 'default'
    if(get_current_db_name()!=None):
        upload_path = get_current_db_name()
    student = ForeignKey(Student, on_delete=CASCADE)
    file =FileField(upload_to='static/uploads/'+upload_path+'/diplom/%Y/%m/%d/')
    created_at = DateTimeField(auto_now_add=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    
