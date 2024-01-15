from django.db.models import CharField,  ForeignKey, BooleanField, PositiveSmallIntegerField, Model, CASCADE

class Menu(Model):
    STATUS_CHOICES = (
        ('OPEN', 'Нээлттэй',),
        ('CLOSED', 'Хаалттай',),
    )
    key = CharField(max_length=50)
    path = CharField(max_length=50)
    title = CharField(max_length=50)
    icon = CharField(max_length=50)
    breadcrumb = BooleanField(blank=False, default=True)
    submenu = ForeignKey("self", on_delete=CASCADE, blank=True, null=True)
    status = CharField(
        max_length=10,
        choices=STATUS_CHOICES,
    )
    priority = PositiveSmallIntegerField(default=1000)
    
    def __str__(self):
        return 'id: '+str(self.pk)+' | title: '+self.title

    class Meta:
        permissions = [
            ("view_home", "View home"),
            ("configs", "Configs tab"),
            ("view_student_report", "View Student report"),
            ("view_mark_report", "View mark report"),
            ("view_report", "View report"),
        ]