import email
import graphene
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from .models import Student, Transfer
from apps.core.models import City, District, Student_status, Student_status_extra, Activity, Degree, Classtime
from apps.teacher.models import Teacher
from apps.school.models import School
from apps.program.models import Program
from apps.classes.models import Classes
from apps.section.models import Section
from apps.schoolyear.models import Schoolyear
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from graphql_jwt.decorators import login_required, permission_required, staff_member_required
from django.db.models import Q

class StudentType(DjangoObjectType):
    class Meta:
        model = Student

class TransferType(DjangoObjectType):
    class Meta:
        model = Transfer

class Query(object):
    all_students_report = graphene.List(
        StudentType
    )
    all_students = graphene.List(
        StudentType, 
        program=graphene.Int(required=False, default_value=0),
        classes=graphene.Int(required=False, default_value=0),
        filter=graphene.String(required=False, default_value='')
    )
    student_by_id = graphene.Field(StudentType, id=graphene.Int(required=True))
    transfers_by_student = graphene.List(TransferType, student=graphene.Int(required=True))
    set_students_paid = graphene.List(StudentType, course=graphene.Int(required=True))

    @login_required
    @staff_member_required
    def resolve_set_students_paid(self, info, course):
        Student.objects.filter(classes__course=course).update(is_paid=True)
        return Student.objects.filter(classes__course=course)

    @login_required
    def resolve_all_students_report(self, info):
        return Student.objects.all()

    @login_required
    def resolve_all_students(self, info, program, classes, filter):

        fields = Student.filter_fields()

        Qr = None
        for field in fields:
            q = Q(**{"%s__icontains" % field: filter })
            if Qr:
                Qr = Qr | q
            else:
                Qr = q

        # if info.context.user.is_superuser==True:
        #     return Student.objects.filter(Qr)

        IDQr = Q()

        if not program==0:
            IDQr = Q(program=program)

        if not classes==0:
            IDQr = Q(classes=classes)
            
        if info.context.user.is_student==True:
            return Student.objects.filter(Q(user=info.context.user), Qr)
        if info.context.user.is_parent==True:
            return Student.objects.filter(id=info.context.user.parent.student.id)
        if info.context.user.is_teacher==True:
            students = Student.access_student(Teacher.objects.get(user=info.context.user))
            if students is None:
                return None
            else:
                return Student.objects.filter(Q(pk__in=students), Qr)
        else: 
            return Student.objects.filter(IDQr, Qr)

    @login_required
    @permission_required('student.view_student')
    def resolve_student_by_id(root, info, id):
        if info.context.user.is_student==True:
            return Student.objects.get(user=info.context.user)
        else:
            return Student.objects.get(id=id)

    @login_required
    @permission_required('student.change_student')
    def resolve_transfers_by_student(root, info, student):
        try:
            return Transfer.objects.filter(student_id=student)
        except Transfer.DoesNotExist:
            return None

#******************* 😎 Student-MUTATIONS 😎 *************************#
class CreateStudent(graphene.Mutation):
    student = graphene.Field(StudentType)

    class Arguments:
        student_code = graphene.String()
        registerNo = graphene.String()
        family_name = graphene.String()
        name = graphene.String()
        photo = Upload()
        phone = graphene.String()
        phone2 = graphene.String()
        address = graphene.String(required=False, default_value="")
        join_date = graphene.String(required=False, default_value=None)
        join_schoolyear = graphene.String()
        join_before = graphene.String()
        sex = graphene.String()
        classtime = graphene.Int()
        status = graphene.Int()
        status_extra = graphene.Int()
        degree = graphene.Int()
        activity = graphene.Int()
        birthdate = graphene.String(required=False, default_value=None)
        birth_city = graphene.Int(required=False, default_value=0)
        birth_district = graphene.Int(required=False, default_value=0)
        school = graphene.Int()
        program = graphene.Int()
        classes = graphene.Int()
        section = graphene.Int()

        password = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    @login_required
    @permission_required('student.add_student')
    def mutate(self, info, student_code, registerNo, family_name, name, phone, phone2, address, join_date, join_schoolyear, join_before, sex, classtime, status, status_extra, degree, activity, birthdate, birth_city, birth_district, school, program, classes, section, password, username, email, photo = ''):

        join_schoolyear_i = Schoolyear.objects.get(pk=join_schoolyear)
        classtime_i = Classtime.objects.get(pk=classtime)
        status_i = Student_status.objects.get(pk=status)
        status_extra_i = Student_status_extra.objects.get(pk=status_extra)
        degree_i = Degree.objects.get(pk=degree)
        activity_i = Activity.objects.get(pk=activity)
        school_i = School.objects.get(pk=school)
        program_i = Program.objects.get(pk=program)
        classes_i = Classes.objects.get(pk=classes)
        section_i = Section.objects.get(pk=section)
        create_userID_i = info.context.user
        
        userob = get_user_model()(username=username,email=email,first_name=family_name,last_name=name,is_student=True,is_teacher=False,is_parent=False,)
        userob.set_password(password)
        userob.save()
        user_i = get_user_model().objects.get(pk=userob.pk)

        group = Group.objects.get(pk=2)
        group.user_set.add(user_i)
        stu = Student(user=user_i, student_code=student_code, registerNo=registerNo, family_name=family_name, name=name, phone=phone, phone2=phone2, address=address, join_schoolyear=join_schoolyear_i,join_before=join_before, sex=sex, classtime=classtime_i, status=status_i, status_extra=status_extra_i, degree=degree_i, activity=activity_i, school=school_i, program=program_i, classes=classes_i, section=section_i, create_userID=create_userID_i)

        try:
            birth_city_i = City.objects.get(pk=birth_city)
            stu.birth_city = birth_city_i
        except City.DoesNotExist:
            print('none')
            
        try:
            birth_district_i = District.objects.get(pk=birth_district)
            stu.birth_district = birth_district_i
        except District.DoesNotExist:
            print('none')

        if not join_date:
            stu.join_date = None
        else:
            stu.join_date = None

        if not birthdate:
            stu.birthdate = None
        else:
            stu.birthdate = None

        stu.save()

        return CreateStudent(student=stu)

class UpdateStudent(graphene.Mutation):
    student = graphene.Field(StudentType)

    class Arguments:
        student_code = graphene.String()
        registerNo = graphene.String()
        family_name = graphene.String()
        name = graphene.String()
        photo = Upload()
        phone = graphene.String()
        phone2 = graphene.String()
        address = graphene.String(required=False, default_value="")
        join_date = graphene.String(required=False, default_value=None)
        join_schoolyear = graphene.String()
        join_before = graphene.String()
        sex = graphene.String()
        degree = graphene.Int()
        birthdate = graphene.String(required=False, default_value=None)
        birth_city = graphene.Int(required=False, default_value=0)
        birth_district = graphene.Int(required=False, default_value=0)
        username = graphene.String()
        email = graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('student.change_student')
    def mutate(self, info, photo='', **kwargs):

        student = Student.objects.get(pk=kwargs["id"])

        user_o = get_user_model().objects.get(pk = student.user_id)

        user_o.username = kwargs["username"]
        user_o.email = kwargs["email"]
        user_o.is_student = True
        user_o.save()

        student.student_code = kwargs["student_code"]
        student.registerNo = kwargs["registerNo"]
        student.family_name = kwargs["family_name"]
        student.name = kwargs["name"]
        if photo != '':
            student.photo = photo
        student.phone = kwargs["phone"]
        student.phone2 = kwargs["phone2"]
        student.address = kwargs["address"]
        student.join_schoolyear_id = kwargs["join_schoolyear"]
        student.join_before = kwargs["join_before"]
        student.sex = kwargs["sex"]
        student.degree_id = kwargs["degree"]

        try:
            birth_city_i = City.objects.get(pk=kwargs["birth_city"])
            student.birth_city = birth_city_i
        except City.DoesNotExist:
            print('none')
            
        try:
            birth_district_i = District.objects.get(pk=kwargs["birth_district"])
            student.birth_district = birth_district_i
        except District.DoesNotExist:
            print('none')

        if not kwargs["join_date"]:
            student.join_date = None
        else:
            student.join_date = None

        if not kwargs["birthdate"]:
            student.birthdate = None
        else:
            student.birthdate = None

        student.save()
        return UpdateStudent(student=student)

class DeleteStudent(graphene.Mutation):
    student = graphene.Field(StudentType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('student.delete_student')
    def mutate(self, info, **kwargs):
        student = Student.objects.get(pk=kwargs["id"])
        if student is not None:
            userob = get_user_model()(pk = student.user_id)
            userob.delete()
            student.delete()
        return DeleteStudent(student=student)

#******************* 😎 Transfer-MUTATIONS 😎 *************************#
class TransferStudent(graphene.Mutation):
    transfer = graphene.Field(TransferType)

    class Arguments:
        student = graphene.Int()
        status = graphene.Int()
        status_extra = graphene.Int()
        classtime = graphene.Int()
        activity = graphene.Int()
        school = graphene.Int()
        program = graphene.Int()
        classes = graphene.Int()
        section = graphene.Int()
        doc_date = graphene.String()
        doc_num = graphene.String()
        description = graphene.String()

    @login_required
    @permission_required('student.change_student')
    def mutate(self, info, student, status, status_extra, classtime, activity, school, program, classes, section, doc_date, doc_num, description):

        student_i = Student.objects.get(pk=student)

        transfer_i = Transfer(student=student_i, status_id=status, status_extra_id=status_extra, classtime_id=classtime, activity_id=activity, school_id=school, program_id=program, classes_id=classes, section_id=section,doc_date=doc_date, doc_num=doc_num, description=description,old_data = str(student_i), create_userID=info.context.user)
        transfer_i.save()

        return TransferStudent(transfer=transfer_i)

class Mutation(graphene.ObjectType):
    create_student = CreateStudent.Field()
    update_student = UpdateStudent.Field()
    delete_student = DeleteStudent.Field()
    transfer_student = TransferStudent.Field()