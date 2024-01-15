import email
from tokenize import group
import graphene
from graphene_django.types import DjangoObjectType
from .models import City, District, Khoroo, Student_status, Teacher_status, Student_status_extra, Activity, Degree, Classtime, Employee_compartment
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required, permission_required
from django.apps import apps
from apps.teacher.models import Teacher
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from itertools import chain

class Count(graphene.ObjectType):
    count = graphene.Int()

class Employee_compartmentType(DjangoObjectType):
    class Meta:
        model = Employee_compartment

class CityType(DjangoObjectType):
    class Meta:
        model = City
        
class DistrictType(DjangoObjectType):
    class Meta:
        model = District

class KhorooType(DjangoObjectType):
    class Meta:
        model = Khoroo

class Student_statusType(DjangoObjectType):
    class Meta:
        model = Student_status

class Teacher_statusType(DjangoObjectType):
    class Meta:
        model = Teacher_status

class Student_status_extraType(DjangoObjectType):
    class Meta:
        model = Student_status_extra

class ActivityType(DjangoObjectType):
    class Meta:
        model = Activity

class DegreeType(DjangoObjectType):
    class Meta:
        model = Degree

class ClasstimeType(DjangoObjectType):
    class Meta:
        model = Classtime

class CustomPermissionType(graphene.ObjectType):
    name = graphene.String()
    code_name = graphene.String()
    add = graphene.Boolean()
    change = graphene.Boolean()
    delete = graphene.Boolean()
    view = graphene.Boolean()

class PermissionType(DjangoObjectType):
    class Meta:
        model = Permission
        
class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "first_name", "last_name", "email", "is_teacher", "is_employee", "is_student", "employee", "teacher", "student", "status", "groups")

class Query(object):
    count = graphene.Field(Count, app_name=graphene.String(required=True), model_name=graphene.String(required=True), filter=graphene.String())
    all_citys = graphene.List(CityType)
    all_districts = graphene.List(DistrictType)
    all_khoroos = graphene.List(KhorooType)
    all_student_statuss = graphene.List(Student_statusType)
    all_teacher_statuss = graphene.List(Teacher_statusType)
    all_student_status_extras = graphene.List(Student_status_extraType)
    all_activitys = graphene.List(ActivityType)
    all_degrees = graphene.List(DegreeType)
    all_classtimes = graphene.List(ClasstimeType)
    permissions = graphene.List(CustomPermissionType)
    all_permissions = graphene.List(PermissionType)
    custom_user_permissions = graphene.List(PermissionType, user_id=graphene.Int(required=False, default_value=0))
    user_permissions = graphene.List(PermissionType)
    group_permissions = graphene.List(PermissionType, user_id=graphene.Int(required=False, default_value=0), group_id=graphene.Int(required=False, default_value=0))
    all_users = graphene.List(UserType)
    all_groups = graphene.List(GroupType)
    user_by_username = graphene.Field(UserType, username=graphene.String(required=True))
    all_attendace_employees = graphene.List(UserType)
    all_employees_compartment = graphene.List(Employee_compartmentType)

    @login_required
    def resolve_all_employees_compartment(self, info):
        return Employee_compartment.objects.all()

    @login_required
    def resolve_all_attendace_employees(self, info):
        users = get_user_model().objects.filter(Q(is_teacher = True) | Q(is_employee = True))
        return users

    @login_required
    def resolve_count(self, info, app_name, model_name, filter):
        model = apps.get_model(app_name, model_name)

        fields = model.filter_fields()

        Qr = None
        for field in fields:
            q = Q(**{"%s__icontains" % field: filter })
            if Qr:
                Qr = Qr | q
            else:
                Qr = q

        if info.context.user.is_superuser==True:
            return { "count": model.objects.filter(Qr).count()}
            
        if info.context.user.is_student==True:
            return { "count": model.objects.filter(Qr).count()}
        else:
            return { "count": model.objects.filter(Qr).count()}
            # students = model.access_student(model2.objects.get(user=info.context.user))
            # if students is None:
            #     return None
            # else:
            #     return { "count": model.objects.filter(pk__in=students).count()}

    @login_required
    def resolve_all_citys(self, info, **kwargs):
        return City.objects.all()

    @login_required
    def resolve_all_districts(self, info, **kwargs):
        return District.objects.all()

    @login_required
    def resolve_all_khoroos(self, info, **kwargs):
        return Khoroo.objects.all()

    @login_required
    def resolve_all_student_statuss(self, info, **kwargs):
        return Student_status.objects.all()

    @login_required
    def resolve_all_teacher_statuss(self, info, **kwargs):
        return Teacher_status.objects.all()

    @login_required
    def resolve_all_student_status_extras(self, info, **kwargs):
        return Student_status_extra.objects.all()

    @login_required
    def resolve_all_activitys(self, info, **kwargs):
        return Activity.objects.all()

    @login_required
    def resolve_all_degrees(self, info, **kwargs):
        return Degree.objects.all()

    @login_required
    def resolve_all_classtimes(self, info, **kwargs):
        return Classtime.objects.all()

    @login_required
    def resolve_all_users(self, info):
        users = get_user_model().objects.all()
        return users

    @login_required
    def resolve_user_by_username(self, info, username):
        user = get_user_model().objects.get(username=username)
        return user

    @login_required
    def resolve_permissions(self, info, **kwargs):

        return [{
        "name":'Хандах эрх',
        "code_name":'permission',
        "add":0,
        "change":1,
        "delete":0,
        "view":0,
        },
        {
        "name":'Хэрэглэгчийн грүпп',
        "code_name":'group',
        "add":0,
        "change":1,
        "delete":0,
        "view":1,
        },
        # {
        # "name":'Хэрэглэгч',
        # "code_name":'customuser',
        # "add":1,
        # "change":1,
        # "delete":1,
        # "view":1,
        # },
        {
        "name":'Анги',
        "code_name":'classes',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Суралцах хэлбэр',
        "code_name":'classtime',
        "add":1,
        "change":1,
        "delete":0,
        "view":1,
        },
        {
        "name":'Зэрэг',
        "code_name":'degree',
        "add":1,
        "change":1,
        "delete":0,
        "view":1,
        },
        {
        "name":'Суралцагчийн төлөв',
        "code_name":'student_status',
        "add":1,
        "change":1,
        "delete":0,
        "view":1,
        },
        {
        "name":'Суралцагчийн нэмэлт төлөв',
        "code_name":'student_status_extra',
        "add":1,
        "change":1,
        "delete":0,
        "view":1,
        },
        {
        "name":'Багшийн төлөв',
        "code_name":'teacher_status',
        "add":1,
        "change":1,
        "delete":0,
        "view":1,
        },
        {
        "name":'Үйл ажиллагааны төрөл',
        "code_name":'event_type',
        "add":1,
        "change":1,
        "delete":0,
        "view":1,
        },
        {
        "name":'Үйл ажиллагаа',
        "code_name":'event',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Онлайн уулзалт',
        "code_name":'live',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Дүнгийн поток',
        "code_name":'mark_board',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Нүүр хуудас',
        "code_name":'home',
        "add":0,
        "change":0,
        "delete":0,
        "view":1,
        },
        {
        "name":'Суралцагчийн тодоройлолт',
        "code_name":'student_report',
        "add":0,
        "change":0,
        "delete":0,
        "view":1,
        },
        {
        "name":'Дүнгийн тодорхойлолт',
        "code_name":'mark_report',
        "add":0,
        "change":0,
        "delete":0,
        "view":1,
        },
        {
        "name":'Онлайн файл',
        "code_name":'online_file',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Онлайн хичээл',
        "code_name":'online_lesson',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Онлайн хичээлийн материал',
        "code_name":'online_sub',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Оюутан, суралцагч',
        "code_name":'student',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Шалгалтын сан',
        "code_name":'online_test',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Шалгалтын асуулт',
        "code_name":'question',
        "add":1,
        "change":0,
        "delete":1,
        "view":0,
        },
        {
        "name":'Асран хамгаалагч',
        "code_name":'parent',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Хөтөлбөр',
        "code_name":'program',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Хичээлийн хуваарь',
        "code_name":'routine',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Бүрэлдхүүн сургууль',
        "code_name":'school',
        "add":0,
        "change":0,
        "delete":0,
        "view":1,
        },
        {
        "name":'Хичээлийн жил',
        "code_name":'schoolyear',
        "add":1,
        "change":1,
        "delete":0,
        "view":1,
        },
        {
        "name":'Суралцагчийн шилжилт хөдөлгөөн',
        "code_name":'transfer',
        "add":1,
        "change":0,
        "delete":0,
        "view":1,
        },
        {
        "name":'Тэнхим',
        "code_name":'sub_school',
        "add":1,
        "change":1,
        "delete":0,
        "view":1,
        },
        {
        "name":'Хичээлийн сан',
        "code_name":'subject',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Хичээлийн сан',
        "code_name":'subject',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Ажилчин',
        "code_name":'employee',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Ажилчдын ирц',
        "code_name":'employee_attandance',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        },
        {
        "name":'Багш',
        "code_name":'teacher',
        "add":1,
        "change":1,
        "delete":1,
        "view":1,
        }]
          
    @login_required
    def resolve_all_permissions(self, info, **kwargs):
        return Permission.objects.all()

    @login_required
    def resolve_group_permissions(self, info, user_id, group_id):
        if user_id != 0:
            user_i = get_user_model().objects.get(pk=user_id)
            return Permission.objects.filter(group__user=user_i)
        elif group_id != 0:
            group = Group.objects.get(pk=group_id)
            return Permission.objects.filter(group=group)
        else:
            return None

    
    @login_required
    def resolve_custom_user_permissions(self, info, user_id):
        user_i = get_user_model().objects.get(pk=user_id)
        return user_i.user_permissions.all()

    @login_required
    # @permission_required('group.view_group')
    def resolve_all_groups(self, info, **kwargs):
        return Group.objects.all()
    
    @login_required
    def resolve_user_permissions(self, info, **kwargs):

        if info.context.user.is_superuser:
            return Permission.objects.all()

        return list(chain(info.context.user.user_permissions.all(), Permission.objects.filter(group__user=info.context.user)))

class ChangeUserPassword(graphene.Mutation):
    user = graphene.Field(UserType)
    class Arguments:
        password = graphene.String()
        id = graphene.Int()

    @login_required
    @permission_required('account.change_user_password')
    def mutate(self, info, password, id):
        user_o = get_user_model().objects.get(pk=id)
        user_o.set_password(password)
        user_o.save()
        return ChangeUserPassword(user=user_o)

class UpdateUserAccount(graphene.Mutation):
    account = graphene.Field(UserType)
    class Arguments:
        id = graphene.Int()
        username = graphene.String()
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()

    @login_required
    @permission_required('customuser.change_customuser')
    def mutate(self, info, **kwargs):
        account = get_user_model().objects.get(pk=kwargs["id"])
        account.email = kwargs["email"]
        account.username = kwargs["username"]
        account.first_name = kwargs["first_name"]
        account.last_name = kwargs["last_name"]
        account.verified = True
        account.save()
        return UpdateUserAccount(account=account)

class Update_group_permission(graphene.Mutation):
    group = graphene.Field(GroupType)

    class Arguments:
        codename = graphene.String()
        id = graphene.ID()
        action = graphene.Boolean()

    @login_required
    @permission_required('permission.change_permission')
    def mutate(self, info, codename, action, id):
        group = Group.objects.get(pk = id)
        permission = Permission.objects.get(codename=codename)
        if action == True:
            group.permissions.add(permission)
        elif action == False:
            group.permissions.remove(permission)
        return Update_group_permission(group=group)

class Update_teacher_permission(graphene.Mutation):
    permission = graphene.Field(PermissionType)

    class Arguments:
        codename = graphene.String()
        teacher_code = graphene.String()
        action = graphene.Boolean()

    @login_required
    @permission_required('permission.change_permission')
    def mutate(self, info, codename, teacher_code, action):
        teacher = Teacher.objects.get(teacher_code=teacher_code)
        user = get_user_model().objects.get(pk=teacher.user.id)
        permission = Permission.objects.get(codename=codename)
        if action == True:
            user.user_permissions.add(permission)
        elif action == False:
            user.user_permissions.remove(permission)
        return Update_teacher_permission(permission=permission)

class CreateCity(graphene.Mutation):
    city = graphene.Field(CityType)

    class Arguments:
        code = graphene.String()
        name = graphene.String()

    @login_required
    def mutate(self, info, code, name):
        cti = City(code = code, name=name)
        cti.save()
        return CreateCity(city=cti)

class CreateDistrict(graphene.Mutation):
    district = graphene.Field(DistrictType)
    class Arguments:
        code = graphene.String()
        name = graphene.String()
        cityID = graphene.Int()
        
    @login_required
    def mutate(self, info, code, name, cityID):
        city_i = City.objects.get(id=cityID)
        dis = District(code=code, name=name, cityID=city_i)
        dis.save()
        return CreateDistrict(district=dis)

class CreateKhoroo(graphene.Mutation):
    khoroo = graphene.Field(KhorooType)
    class Arguments:
        name = graphene.String()
        districtID = graphene.Int()
        cityID = graphene.Int()
        
    @login_required
    def mutate(self, info, name, districtID, cityID):
        city_i = City.objects.get(id=cityID)
        district_i = District.objects.get(id=districtID)
        khr = Khoroo(name=name, cityID=city_i, districtID=district_i)
        khr.save()
        return CreateKhoroo(khoroo=khr)

class CreateStudent_status(graphene.Mutation):
    student_status = graphene.Field(Student_statusType)
    class Arguments:
        name = graphene.String()
        
    @login_required
    def mutate(self, info, name):
        ssa = Student_status( name=name)
        ssa.save()
        return CreateStudent_status(student_status=ssa)

class CreateTeacher_status(graphene.Mutation):
    teacher_status = graphene.Field(Teacher_statusType)
    class Arguments:
        name = graphene.String()
        
    @login_required
    def mutate(self, info, name):
        tsa = Teacher_status(name=name)
        tsa.save()
        return CreateTeacher_status(teacher_status=tsa)

class CreateStudent_status_extra(graphene.Mutation):
    student_status_extra = graphene.Field(Student_status_extraType)
    class Arguments:
        name = graphene.String()
        
    @login_required
    def mutate(self, info, name):
        sse = Student_status_extra(name=name)
        sse.save()
        return CreateStudent_status_extra(student_status_extra=sse)

class CreateActivity(graphene.Mutation):
    activity = graphene.Field(ActivityType)
    class Arguments:
        name = graphene.String()
        
    @login_required
    def mutate(self, info, name):
        act = Activity(name=name)
        act.save()
        return CreateActivity(activity=act)

class CreateDegree(graphene.Mutation):
    degree = graphene.Field(DegreeType)
    class Arguments:
        name = graphene.String()
        
    @login_required
    def mutate(self, info, name):
        dgr = Degree(name=name)
        dgr.save()
        return CreateDegree(degree=dgr)

class CreateClasstime(graphene.Mutation):
    classtime = graphene.Field(ClasstimeType)
    class Arguments:
        name = graphene.String()
        
    @login_required
    def mutate(self, info, name):
        cla = Classtime(name=name)
        cla.save()
        return CreateClasstime(classtime=cla)


class UpdateCity(graphene.Mutation):
    city = graphene.Field(CityType)

    class Arguments:
        code = graphene.String()
        name = graphene.String()
        id = graphene.ID()

    @login_required
    def mutate(self, info, code, name, id):
        city = City.objects.get(pk=id)
        city.code = code
        city.name = name
        city.save()
        return UpdateCity(city=city)

class UpdateDistrict(graphene.Mutation):
    district = graphene.Field(DistrictType)
    class Arguments:
        code = graphene.String()
        name = graphene.String()
        cityID = graphene.Int()
        id = graphene.ID()

    @login_required
    def mutate(self, info, code, name, cityID, id):
        district = District.objects.get(pk=id)
        city_i = City.objects.get(id=cityID)
        district.code = code
        district.name = name
        district.cityID = city_i
        district.save()

        return UpdateDistrict(district=district)

class UpdateKhoroo(graphene.Mutation):
    khoroo = graphene.Field(KhorooType)
    class Arguments:
        name = graphene.String()
        districtID = graphene.Int()
        cityID = graphene.Int()
        id = graphene.ID()

    @login_required
    def mutate(self, info, code, name, cityID, districtID, id):
        khoroo = Khoroo.objects.get(pk=id)
        city_i = City.objects.get(id=cityID)
        district_i = District.objects.get(id=districtID)
        khoroo.code = code
        khoroo.name = name
        khoroo.districtID = district_i
        khoroo.cityID = city_i
        khoroo.save()
        return UpdateKhoroo(khoroo=khoroo)

class UpdateStudent_status(graphene.Mutation):
    student_status = graphene.Field(Student_statusType)
    class Arguments:
        name = graphene.String()
        id = graphene.ID()

    @login_required
    def mutate(self, info, name, id):
        student_status = Student_status.objects.get(pk=id)
        student_status.name = name
        student_status.save()
        return UpdateStudent_status(student_status=student_status)

class UpdateTeacher_status(graphene.Mutation):
    teacher_status = graphene.Field(Teacher_statusType)
    class Arguments:
        name = graphene.String()
        id = graphene.ID()

    @login_required
    def mutate(self, info, name, id):
        teacher_status = Teacher_status.objects.get(pk=id)
        teacher_status.name = name
        teacher_status.save()
        return UpdateTeacher_status(teacher_status=teacher_status)

class UpdateStudent_status_extra(graphene.Mutation):
    student_status_extra = graphene.Field(Student_status_extraType)
    class Arguments:
        name = graphene.String()
        id = graphene.ID()

    @login_required
    def mutate(self, info, name, id):
        student_status_extra = Student_status_extra.objects.get(pk=id)
        student_status_extra.name = name
        student_status_extra.save()

        return UpdateStudent_status_extra(student_status_extra=student_status_extra)

class UpdateActivity(graphene.Mutation):
    activity = graphene.Field(ActivityType)
    class Arguments:
        name = graphene.String()
        id = graphene.ID()

    @login_required
    def mutate(self, info, name, id):
        activity = Activity.objects.get(pk=id)
        activity.name = name
        activity.save()

        return UpdateActivity(activity=activity)

class UpdateDegree(graphene.Mutation):
    degree = graphene.Field(DegreeType)
    class Arguments:
        name = graphene.String()
        id = graphene.ID()

    @login_required
    def mutate(self, info, name, id):
        degree = Degree.objects.get(pk=id)
        degree.name = name
        degree.save()
        return UpdateDegree(degree=degree)

class UpdateClasstime(graphene.Mutation):
    classtime = graphene.Field(ClasstimeType)
    class Arguments:
        name = graphene.String()
        id = graphene.ID()

    @login_required
    def mutate(self, info, name, id):
        classtime = Classtime.objects.get(pk=id)
        classtime.name = name
        classtime.save()
        return UpdateClasstime(classtime=classtime)


class DeleteCity(graphene.Mutation):
    city = graphene.Field(CityType)

    class Arguments:
        id = graphene.ID()

    @login_required
    def mutate(self, info, **kwargs):
        city = City.objects.get(pk=kwargs["id"])
        if city is not None:
            city.delete()
        return DeleteCity(city=city)

class DeleteDistrict(graphene.Mutation):
    district = graphene.Field(DistrictType)
    class Arguments:
        id = graphene.ID()

    @login_required
    def mutate(self, info, **kwargs):
        district = District.objects.get(pk=kwargs["id"])
        if district is not None:
            district.delete()
        return DeleteDistrict(district=district)

class DeleteKhoroo(graphene.Mutation):
    khoroo = graphene.Field(KhorooType)
    class Arguments:
        id = graphene.ID()

    @login_required
    def mutate(self, info, **kwargs):
        khoroo = Khoroo.objects.get(pk=kwargs["id"])
        if khoroo is not None:
            khoroo.delete()
        return DeleteKhoroo(khoroo=khoroo)

class DeleteStudent_status(graphene.Mutation):
    student_status = graphene.Field(Student_statusType)
    class Arguments:
        id = graphene.ID()

    @login_required
    def mutate(self, info, **kwargs):
        student_status = Student_status.objects.get(pk=kwargs["id"])
        if student_status is not None:
            student_status.delete()
        return DeleteStudent_status(student_status=student_status)

class DeleteTeacher_status(graphene.Mutation):
    teacher_status = graphene.Field(Teacher_statusType)
    class Arguments:
        id = graphene.ID()

    @login_required
    def mutate(self, info, **kwargs):
        teacher_status = Teacher_status.objects.get(pk=kwargs["id"])
        if teacher_status is not None:
            teacher_status.delete()
        return DeleteTeacher_status(teacher_status=teacher_status)

class DeleteStudent_status_extra(graphene.Mutation):
    student_status_extra = graphene.Field(Student_status_extraType)
    class Arguments:
        id = graphene.ID()

    @login_required
    def mutate(self, info, **kwargs):
        student_status_extra = Student_status_extra.objects.get(pk=kwargs["id"])
        if student_status_extra is not None:
            student_status_extra.delete()
        return DeleteStudent_status_extra(student_status_extra=student_status_extra)

class DeleteActivity(graphene.Mutation):
    activity = graphene.Field(ActivityType)
    class Arguments:
        id = graphene.ID()

    @login_required
    def mutate(self, info, **kwargs):
        activity = Activity.objects.get(pk=kwargs["id"])
        if activity is not None:
            activity.delete()
        return DeleteActivity(activity=activity)

class DeleteDegree(graphene.Mutation):
    degree = graphene.Field(DegreeType)
    class Arguments:
        id = graphene.ID()

    @login_required
    def mutate(self, info, **kwargs):
        degree = Degree.objects.get(pk=kwargs["id"])
        if degree is not None:
            degree.delete()
        return DeleteDegree(degree=degree)

class DeleteClasstime(graphene.Mutation):
    classtime = graphene.Field(ClasstimeType)
    class Arguments:
        id = graphene.ID()

    @login_required
    def mutate(self, info, **kwargs):
        classtime = Classtime.objects.get(pk=kwargs["id"])
        if classtime is not None:
            classtime.delete()
        return DeleteClasstime(classtime=classtime)

        
class DeleteAccount(graphene.Mutation):
    account = graphene.Field(UserType)
    class Arguments:
        username = graphene.String()

    @login_required
    @permission_required('customuser.delete_customuser')
    def mutate(self, info, **kwargs):
        account = get_user_model().objects.get(username=kwargs["username"])
        if account is not None:
            account.delete()
        return DeleteAccount(account=account)

class Mutation(graphene.ObjectType):
    create_city = CreateCity.Field()
    create_district = CreateDistrict.Field()
    create_khoroo = CreateKhoroo.Field()
    create_student_status = CreateStudent_status.Field()
    create_teacher_status = CreateTeacher_status.Field()
    create_student_status_extra = CreateStudent_status_extra.Field()
    create_activity = CreateActivity.Field()
    create_degree = CreateDegree.Field()
    create_classtime = CreateClasstime.Field()
    update_city = UpdateCity.Field()
    update_district = UpdateDistrict.Field()
    update_khoroo = UpdateKhoroo.Field()
    update_student_status = UpdateStudent_status.Field()
    update_teacher_status = UpdateTeacher_status.Field()
    update_student_status_extra = UpdateStudent_status_extra.Field()
    update_activity = UpdateActivity.Field()
    update_degree = UpdateDegree.Field()
    update_classtime = UpdateClasstime.Field()
    delete_city = DeleteCity.Field()
    delete_district = DeleteDistrict.Field()
    delete_khoroo = DeleteKhoroo.Field()
    delete_student_status = DeleteStudent_status.Field()
    delete_teacher_status = DeleteTeacher_status.Field()
    delete_student_status_extra = DeleteStudent_status_extra.Field()
    delete_activity = DeleteActivity.Field()
    delete_degree = DeleteDegree.Field()
    delete_classtime = DeleteClasstime.Field()
    delete_account = DeleteAccount.Field()
    update_teacher_permission = Update_teacher_permission.Field()
    update_group_permission = Update_group_permission.Field()
    update_user_account = UpdateUserAccount.Field()
    change_user_password = ChangeUserPassword.Field()