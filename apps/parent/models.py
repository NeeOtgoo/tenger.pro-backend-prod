from django.db.models import CharField, ForeignKey, DateTimeField, TextField, ImageField, OneToOneField, CASCADE, Model
from apps.student.models import Student
from django.conf import settings

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'static/uploads/photo/user_{0}/{1}'.format(instance.user.id, filename)

class Parent(Model):
    user = OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    family_name = CharField(max_length=50)
    name = CharField(max_length=50)
    photo = ImageField(upload_to=user_directory_path, default='default.jpg')
    profession = CharField(max_length=50)
    phone = CharField(max_length=8, blank=True)
    phone2 = CharField(max_length=8, blank=True)
    address = TextField(blank=True)
    address_live = TextField(blank=True)
    student = ForeignKey(Student, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, related_name = 'parent_create_userID', on_delete=CASCADE)

    def __str__(self):
        return 'family_name: '+self.family_name+' | name: '+str(self.name)

    def filter_fields():
        return ['family_name','name', 'phone','phone2']