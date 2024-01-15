import graphene
from graphene_django.types import DjangoObjectType
from .models import Routine, Routine_student, Routine_time, Routine_attendance
from apps.program.models import Program
from apps.classes.models import Classes
from apps.section.models import Section
from apps.subject.models import Subject
from apps.student.models import Student
from apps.teacher.models import Teacher
from apps.schoolyear.models import Schoolyear
from datetime import date, datetime, timedelta
from graphql_jwt.decorators import login_required, permission_required
from django.db.models import Q

class RoutineType(DjangoObjectType):
    class Meta:
        model = Routine

class Routine_studentType(DjangoObjectType):
    class Meta:
        model = Routine_student

class Routine_timeType(DjangoObjectType):
    class Meta:
        model = Routine_time    

class Routine_attendanceType(DjangoObjectType):
    class Meta:
        model = Routine_attendance

class Query(object):
    routines = graphene.List(RoutineType, filter=graphene.String(required=False, default_value=''))
    all_routine_students = graphene.List(Routine_studentType, routine=graphene.Int(required=True))
    all_routine_times = graphene.List(Routine_timeType, date=graphene.Date(required=False, default_value=datetime.today()))
    all_routine_attendances = graphene.List(Routine_attendanceType, routine_time=graphene.Int(required=True))

    @login_required
    @permission_required('routine.view_routine')
    def resolve_routines(root, info, filter):

        fields = Routine.filter_fields()

        try:
            schoolyear = Schoolyear.objects.get(is_current=True)
        except Schoolyear.DoesNotExist:
            return Routine.objects.none()
            
        Qr = None
        for field in fields:
            q = Q(**{"%s__icontains" % field: filter })
            if Qr:
                Qr = Qr | q
            else:
                Qr = q

        if info.context.user.is_teacher==True:
            teachers = Teacher.access_teacher(Teacher.objects.get(user=info.context.user))
            return Routine.objects.filter(Q(teacher_id__in=teachers), Q(schoolyear_id=schoolyear), Qr)
            
        if info.context.user.is_student==True:
            routines = Routine_student.objects.filter(student=Student.objects.get(user=info.context.user)).values('routine')
            return Routine.objects.filter(Q(pk__in=routines), Q(schoolyear_id=schoolyear), Qr)
        else:
            return Routine.objects.filter(Q(schoolyear_id=schoolyear), Qr)

    @login_required
    @permission_required('routine.view_routine_student')
    def resolve_all_routine_students(root, info, routine):

        return Routine_student.objects.filter(routine=routine)

    @login_required
    @permission_required('routine.view_routine_time')
    def resolve_all_routine_times(root, info, date):

        fields = Routine.filter_fields()

        nxt_mnth = date.replace(day=28) + timedelta(days=4)
        last_date = nxt_mnth - timedelta(days=nxt_mnth.day)

        if info.context.user.is_teacher==True:
            teachers = Teacher.access_teacher(Teacher.objects.get(user=info.context.user))
            routines = Routine.objects.filter(Q(teacher_id__in=teachers))

            return Routine_time.objects.filter(Q(date__range=(date.replace(day=1), last_date)), routine__in = routines).order_by('date', 'time')

        if info.context.user.is_student==True:
            student = Student.objects.get(user=info.context.user)
            routines = Routine_student.objects.filter(student=student).values('routine_id')
            return Routine_time.objects.filter(Q(date__range=(date.replace(day=1), last_date)), routine_id__in=routines).order_by('date', 'time')
        else:
            return Routine_time.objects.filter(Q(date__range=(date.replace(day=1), last_date))).order_by('date', 'time')

    @login_required
    @permission_required('routine.view_all_routine_attendance')
    def resolve_all_routine_attendances(root, info, routine_time):
        if info.context.user.is_student==True:
            student = Student.objects.get(user=info.context.user)
            return Routine_attendance.objects.filter(routine_time=routine_time,student = student)
        else:
            return Routine_attendance.objects.filter(routine_time=routine_time)

#******************* 😎 Routine-MUTATIONS 😎 *************************#
class CreateRoutine(graphene.Mutation):
    routine = graphene.Field(RoutineType)

    class Arguments:
        schoolyear = graphene.Int()
        program = graphene.Int()
        classes = graphene.Int()
        section = graphene.Int()
        subject = graphene.Int()
        teacher = graphene.Int()
        type = graphene.String()
        time = graphene.Int()
        weekly = graphene.Int()
        start_date = graphene.Date()
        end_date = graphene.Date()
        room = graphene.String()

    @login_required
    @permission_required('routine.add_routine')
    def mutate(self, info, schoolyear, program, classes, section, subject, teacher, type, time, weekly, start_date, end_date, room):

        schoolyear_i = Schoolyear.objects.get(pk=schoolyear)
        program_i = Program.objects.get(pk=program)
        classes_i = Classes.objects.get(pk=classes)
        section_i = Section.objects.get(pk=section)
        subject_i = Subject.objects.get(pk=subject)
        teacher_i = Teacher.objects.get(pk=teacher)
        create_userID_i = info.context.user

        routine_o = Routine(schoolyear=schoolyear_i, program=program_i, classes=classes_i, section=section_i, subject=subject_i, teacher=teacher_i, create_userID=create_userID_i)
        routine_o.save()

        routine_inserted = Routine.objects.latest('id')
        if weekly == 0:
            delta = timedelta(days=7)
        else:
            delta = timedelta(days=14)

        while start_date <= end_date:
            routine_time_o = Routine_time(routine=routine_inserted, type=type, time=time, date=start_date, room=room)
            routine_time_o.save()
            start_date += delta

        for student in Student.objects.filter(section=section_i):
            routine_student_o = Routine_student(routine=routine_inserted, student=student)
            routine_student_o.save()

        return CreateRoutine(routine=routine_o)
        
class DeleteRoutine(graphene.Mutation):
    routine = graphene.Field(RoutineType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('routine.delete_routine')
    def mutate(self, info, **kwargs):
        routine = Routine.objects.get(pk=kwargs["id"])
        if routine is not None:
            routine.delete()
        return DeleteRoutine(routine=routine)

#******************* 😎 Routine_student-MUTATIONS 😎 *************************#
class CreateRoutine_student(graphene.Mutation):
    routine_student = graphene.Field(Routine_studentType)

    class Arguments:
        routine = graphene.Int()
        section = graphene.Int()
        student_code = graphene.String()

    @login_required
    @permission_required('routine.add_routine_student')
    def mutate(self, info, routine, section, student_code=''):

        routine_i = Routine.objects.get(pk=routine)

        if(student_code==''):
            for student in Student.objects.filter(section=section):
                routine_student_o = Routine_student(routine=routine_i, student=student)
                routine_student_o.save()
        else:
            student_i = Student.objects.get(student_code=student_code)
            routine_student_o = Routine_student(student=student_i, routine=routine_i)
            routine_student_o.save()

        return CreateRoutine_student(routine_student=routine_student_o)

class DeleteRoutine_student(graphene.Mutation):
    routine_student = graphene.Field(Routine_studentType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('routine.delete_routine_student')
    def mutate(self, info, **kwargs):
        routine_student = Routine_student.objects.get(pk=kwargs["id"])
        if routine_student is not None:
            routine_student.delete()
        return DeleteRoutine(routine_student=routine_student)

class Mutation(graphene.ObjectType):
    create_routine = CreateRoutine.Field()
#    update_routine = UpdateRoutine.Field()
    delete_routine = DeleteRoutine.Field()
    create_routine_student = CreateRoutine_student.Field()
    delete_routine_student = DeleteRoutine_student.Field()