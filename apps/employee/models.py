from django.db.models import CharField, TextField, Model, OneToOneField, CASCADE, ImageField, ForeignKey, DateField, DateTimeField, BooleanField
from apps.core.models import City, District, Employee_compartment, Teacher_status
from django.conf import settings
from tenants.middlewares import get_current_db_name

def user_directory_path(instance, filename):
    upload_path = 'default'
    if(get_current_db_name()!=None):
        upload_path = get_current_db_name()
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'uploads/'+upload_path+'/photo/user_{0}/{1}'.format(instance.user.id, filename)

class Employee(Model):
    user = OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    employee_code = CharField(unique=True, max_length=40)
    family_name = CharField(max_length=100)
    name = CharField(max_length=100)
    registerNo = CharField(max_length=50)
    photo = ImageField(upload_to=user_directory_path, default='default.jpg')
    phone = CharField(max_length=8, blank=True)
    phone2 = CharField(max_length=8, blank=True)
    address = TextField(blank=True)
    sex = CharField(max_length=10)
    birthdate = DateField(blank=True)
    birth_city = ForeignKey(City, on_delete=CASCADE)
    birth_district = ForeignKey(District, on_delete=CASCADE)
    status = ForeignKey(Teacher_status, on_delete=CASCADE)
    compartment = ForeignKey(Employee_compartment, on_delete=CASCADE, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def filter_fields():
        return ['employee_code', 'family_name', 'name', 'registerNo']

    
    def __str__(self):
        return 'id: '+str(self.pk)+' | '+self.name

        
class Employee_attandance(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    is_in = BooleanField(default=True)
    is_out = BooleanField(default=False)
    time_in = DateTimeField(auto_now_add=True)
    time_out = DateTimeField(auto_now=True)

    def __str__(self):
        return 'id: '+str(self.pk)

