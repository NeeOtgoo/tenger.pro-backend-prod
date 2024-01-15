from django.db.models import CharField, ForeignKey, Model, CASCADE

class City(Model):
    code = CharField(max_length=2)
    name = CharField(max_length=50)

    def __str__(self):
        return 'id: '+str(self.pk)+' | '+self.name

class District(Model):
    code = CharField(max_length=4)
    name = CharField(max_length=50)
    cityID = ForeignKey(City, on_delete=CASCADE)

    def __str__(self):
        return 'id: '+str(self.pk)+' | '+self.name

class Khoroo(Model):
    name = CharField(max_length=20)
    cityID = ForeignKey(City, on_delete=CASCADE)
    districtID = ForeignKey(District, on_delete=CASCADE)

    def __str__(self):
        return 'id: '+str(self.pk)+' | '+self.name

class Student_status(Model):
    name = CharField(max_length=80)

    def __str__(self):
        return 'id: '+str(self.pk)+' | '+self.name

class Teacher_status(Model):
    name = CharField(max_length=80)

    def __str__(self):
        return 'id: '+str(self.pk)+' | '+self.name

class Student_status_extra(Model):
    name = CharField(max_length=80)

    def __str__(self):
        return 'id: '+str(self.pk)+' | '+self.name

class Activity(Model):
    name = CharField(max_length=80)

    def __str__(self):
        return 'id: '+str(self.pk)+' | '+self.name

class Degree(Model):
    name = CharField(max_length=80)

    def __str__(self):
        return 'id: '+str(self.pk)+' | '+self.name

class Classtime(Model):
    name = CharField(max_length=80)

    def __str__(self):
        return 'id: '+str(self.pk)+' | '+self.name

class Employee_compartment(Model):
    name = CharField(max_length=80)
    def __str__(self):
        return 'id: '+str(self.pk)+' | '+self.name