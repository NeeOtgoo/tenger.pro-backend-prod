from django.db.models import Model, CharField, DateField, DateTimeField, BooleanField, ForeignKey, CASCADE
from django.conf import settings
# Create your models here.
class Schoolyear(Model):
    schoolyear = CharField(max_length=30)
    season = CharField(max_length=30)
    semester_code = CharField(max_length=30)
    start_date = DateField(auto_now=True)
    end_date = DateField(auto_now=True)
    is_current = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def __str__(self):
        return 'id: '+str(self.pk)+' | schoolyear: '+self.schoolyear+' | season: '+self.season+' | semester_code: '+self.semester_code