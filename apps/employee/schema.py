import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from apps.core.models import City, District, Employee_compartment, Teacher_status
from apps.school.models import School_location
from .models import Employee, Employee_attandance
from graphql_jwt.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from account.models import CustomUser
from datetime import datetime, timedelta, time
import haversine as hs
from haversine import Unit
from django.db.models import Q

class EmployeeType(DjangoObjectType):
    class Meta: 
        model = Employee

class EmployeeAttandaceType(DjangoObjectType):
    class Meta: 
        model = Employee_attandance

class Query(object):
    all_employees = graphene.List(EmployeeType, filter=graphene.String(required=False, default_value=''))
    employees_attandance_by_range = graphene.List(EmployeeAttandaceType, start_date=graphene.DateTime(required=True), end_date=graphene.DateTime(required=True))

    @login_required
    def resolve_all_employees(self, info, filter):
        fields = Employee.filter_fields()
        Qr = None
        for field in fields:
            q = Q(**{"%s__icontains" % field: filter })
            if Qr:
                Qr = Qr | q
            else:
                Qr = q
        return Employee.objects.filter(Qr)
        # if info.context.user.is_superuser==True:
        # if info.context.user.is_employee==True:
        #     employee = Student.objects.get(user=info.context.user)
        #     return Program.objects.filter(pk=student.program_id)
        # else:
        #     # programs = Program.access_program(Teacher.objects.get(user=info.context.user))
        #     # return Program.objects.filter(pk__in=programs)
        #     return Program.objects.all()

    @login_required
    def resolve_employees_attandance_by_range(self, info, start_date, end_date):
        return Employee_attandance.objects.filter(time_in__range=(start_date, end_date))

class TakeAttandaceByQrCode(graphene.Mutation):
    take_attandace_by_qr_code = graphene.String()

    class Arguments:
        qr_data = graphene.String()
    
    def mutate(self, info, qr_data):

        user = CustomUser.objects.get(username=qr_data)

        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())

        try: 
            today_attandance = Employee_attandance.objects.get(time_in__lte=today_end, time_out__gte=today_start, user=user)
            attandance_o = Employee_attandance.objects.get(pk=today_attandance.id)
            attandance_o.is_out = True

            attandance_o.save()
            return TakeAttandaceByQrCode('Баяртай сайхан амраарай')
        except Employee_attandance.DoesNotExist:
            attandance_o = Employee_attandance(user=user)
            attandance_o.save()
            return TakeAttandaceByQrCode('Амжилттай бүртгэгдлээ өдрийг сайхан өнгөрүүлээрэй')

class CreateOrUpdateAttandace(graphene.Mutation):
    create_or_update_attandace =  graphene.String()

    class Arguments:
        lon = graphene.Float()
        lat = graphene.Float()
        
    @login_required
    def mutate(self, info, lon, lat):

        user_i = info.context.user

        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())
        
        school_loc = School_location.objects.all().last()

        loc1=(school_loc.lon, school_loc.lat)
        loc2=(lon, lat)
        
        diff_location =  hs.haversine(loc1,loc2,unit=Unit.METERS)

        if (diff_location > 500):
            return CreateOrUpdateAttandace('Таны байгаа байршил тохирохгүй байна!')

        try:
            today_attandance = Employee_attandance.objects.get(time_in__lte=today_end, time_out__gte=today_start, user=user_i)
            attandance_o = Employee_attandance.objects.get(pk=today_attandance.id)
            attandance_o.is_out = True

            attandance_o.save()
            return CreateOrUpdateAttandace('Баяртай сайхан амраарай')

        except Employee_attandance.DoesNotExist:
            attandance_o = Employee_attandance(user=user_i)
            attandance_o.save()
            return CreateOrUpdateAttandace('Амжилттай бүртгэгдлээ өдрийг сайхан өнгөрүүлээрэй')

class CreateEmployee(graphene.Mutation):
    employee = graphene.Field(EmployeeType)

    class Arguments:
        employee_code = graphene.String(required=True)
        family_name = graphene.String()
        name = graphene.String()
        registerNo = graphene.String()
        photo = Upload()
        phone = graphene.String()
        phone2 = graphene.String()
        address = graphene.String()
        sex = graphene.String()
        birthdate = graphene.String()
        birth_city = graphene.Int()
        birth_district = graphene.Int()
        status = graphene.Int()
        group = graphene.Int()
        compartment = graphene.Int()

        password = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    @login_required
    @permission_required('employee.add_employee')
    def mutate(self, info, employee_code, compartment, family_name, name, registerNo, phone, phone2, address, sex, birthdate, birth_city, birth_district, status, group, password, username, email, photo=''):
        
        birth_city_i = City.objects.get(pk=birth_city)
        birth_district_i = District.objects.get(pk=birth_district)
        status_i = Teacher_status.objects.get(pk=status)
        
        userob = get_user_model()(username=username,email=email,first_name=family_name,last_name=name,is_student=False,is_teacher=False,is_parent=False,is_employee=True)
        userob.set_password(password)
        userob.save()
        user_i = get_user_model().objects.get(pk=userob.pk)

        compartment_o = Employee_compartment.objects.get(pk=compartment)

        group_i = group
        group = Group.objects.get(pk=group_i)
        group.user_set.add(user_i)

        employee_o = Employee(user=user_i, employee_code=employee_code, compartment=compartment_o, family_name=family_name, name=name, registerNo=registerNo, phone=phone, phone2=phone2, address=address, sex=sex, birthdate=birthdate, birth_city=birth_city_i, birth_district=birth_district_i, status=status_i)

        # if photo != '':
        #     employee_o.photo = photo

        employee_o.save()
        return CreateEmployee(employee=employee_o)

class UpdateEmployee(graphene.Mutation):
    employee = graphene.Field(EmployeeType)

    class Arguments:
        employee_code = graphene.String()
        family_name = graphene.String()
        name = graphene.String()
        registerNo = graphene.String()
        phone = graphene.String()
        phone2 = graphene.String()
        address = graphene.String()
        sex = graphene.String()
        birthdate = graphene.String()
        birth_city = graphene.Int()
        birth_district = graphene.Int()
        status = graphene.Int()
        group = graphene.Int()
        compartment = graphene.Int()
        username = graphene.String()
        email = graphene.String()
        id = graphene.Int()

    @login_required
    @permission_required('employee.change_employee')
    def mutate(self, info, **kwargs):

        employee = Employee.objects.get(pk=kwargs["id"])
        compartment_o = Employee_compartment.objects.get(pk=kwargs["compartment"])
        user_o = get_user_model().objects.get(pk = employee.user_id)

        user_o.username = kwargs["username"]
        user_o.email = kwargs["email"]
        user_o.set_password(kwargs["username"])
        user_o.is_employee = True
        user_o.save()

        employee.employee_code = kwargs["employee_code"]
        employee.family_name = kwargs["family_name"]
        employee.name = kwargs["name"]
        employee.registerNo = kwargs["registerNo"]
        employee.compartment = compartment_o
        employee.phone = kwargs["phone"]
        employee.phone2 = kwargs["phone2"]
        employee.address = kwargs["address"]
        employee.sex = kwargs["sex"]
        employee.birth_city_id = kwargs["birth_city"]
        employee.birth_district_id = kwargs["birth_district"]
        employee.status_id = kwargs["status"]
        employee.save()

        return UpdateEmployee(employee=employee)

        # if photo != '':
        #     employee_o.photo = photo

class DeleteEmployee(graphene.Mutation):
    employee = graphene.Field(EmployeeType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('employee.delete_employee')
    def mutate(self, info, **kwargs):
        employee = Employee.objects.get(pk=kwargs["id"])
        if employee is not None:
            userob = get_user_model()(pk = employee.user_id)
            userob.delete()
            employee.delete()
        return DeleteEmployee(employee=employee)

class Mutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field()
    update_employee = UpdateEmployee.Field()
    delete_employee = DeleteEmployee.Field()
    create_or_update_attandace = CreateOrUpdateAttandace().Field()
    take_attandace_by_qr_code = TakeAttandaceByQrCode().Field()