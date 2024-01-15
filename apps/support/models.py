from django.db.models import Model, CharField, TextField, ForeignKey, CASCADE, FileField
from django.contrib.auth.models import Group
from tenants.middlewares import get_current_db_name

# Create your models here.
class Support(Model):
    title = CharField(max_length=200)
    description = TextField(blank=True)

class SupportFile(Model):
    upload_path = 'default'
    if(get_current_db_name()!=None):
        upload_path = get_current_db_name()
    file =FileField(upload_to='static/uploads/'+upload_path+'/supports/%Y/%m/%d/', max_length=500)
    support = ForeignKey(Support, on_delete=CASCADE)

class SupportGroup(Model):
    support = ForeignKey(Support, on_delete=CASCADE)
    group = ForeignKey(Group, on_delete=CASCADE)

