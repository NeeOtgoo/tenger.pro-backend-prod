import graphene
from graphene_django.types import DjangoObjectType
from .models import Classes
from apps.sub_school.models import Sub_school
from apps.school.models import School
from apps.program.models import Program
from apps.teacher.models import Teacher
from apps.section.models import Section
from apps.student.models import Student
from apps.core.models import Degree, Activity
from graphql_jwt.decorators import login_required, permission_required
from django.db.models import Q

class ClassesType(DjangoObjectType):
    class Meta:
        model = Classes

class Query(object):
    all_classess = graphene.List(ClassesType, program=graphene.Int(required=False, default_value=0), offset=graphene.Int(required=False, default_value=0), limit=graphene.Int(required=False, default_value=50), filter=graphene.String(required=False, default_value=''))
    classes_by_id = graphene.Field(ClassesType, id=graphene.Int(required=True))

    @login_required
    def resolve_all_classess(self, info, program, offset, limit, filter):

        fields = Classes.filter_fields()

        Qr = None
        for field in fields:
            q = Q(**{"%s__icontains" % field: filter })
            if Qr:
                Qr = Qr | q
            else:
                Qr = q

        if info.context.user.is_superuser==True:
            if program == 0:
                return Classes.objects.filter(Qr)[offset:limit]
            else:
                return Classes.objects.filter(program_id = program)
            
        if info.context.user.is_student==True:
            student = Student.objects.get(user=info.context.user)
            return Classes.objects.filter(pk=student.classes_id)
        else:
            # teachers = Teacher.access_teacher(Teacher.objects.get(user=info.context.user))
            # return Classes.objects.filter(teacher_id__in=teachers, program_id = program)
            if program == 0:
                return Classes.objects.filter(Qr)[offset:limit]
            else:
                return Classes.objects.filter(program_id = program)

    @login_required
    @permission_required('classes.view_classes')
    def resolve_classes_by_id(root, info, id):
        try:
            return Classes.objects.get(id=id)
        except Classes.DoesNotExist:
            return None

#******************* 😎 Classes-MUTATIONS 😎 *************************#
class CreateClasses(graphene.Mutation):
    classes = graphene.Field(ClassesType)

    class Arguments:
        classes = graphene.String()
        classes_mgl = graphene.String()
        classes_numeric = graphene.String()
        degree = graphene.Int()
        activity = graphene.Int()
        max_student_num = graphene.Int()
        teacher = graphene.Int()
        program = graphene.Int()
        sub_school = graphene.Int()
        school = graphene.Int()
        status = graphene.String()
        course = graphene.Int()
        end_course = graphene.Int()

    @login_required
    @permission_required('classes.add_classes')
    def mutate(self, info, classes, classes_mgl, classes_numeric, degree, activity, max_student_num, teacher, program, sub_school, school, status, course, end_course):
        
        degree_i = Degree.objects.get(pk=degree)
        activity_i = Activity.objects.get(pk=activity)
        teacher_i = Teacher.objects.get(pk=teacher)
        program_i = Program.objects.get(pk=program)
        sub_school_i = Sub_school.objects.get(pk=sub_school)
        school_i = School.objects.get(pk=school)
        create_userID_i = info.context.user

        cla = Classes(classes=classes, classes_mgl=classes_mgl, classes_numeric=classes_numeric, degree=degree_i, activity=activity_i, max_student_num=max_student_num, teacher=teacher_i, program=program_i, sub_school=sub_school_i, school=school_i, status=status, course=course, end_course=end_course, create_userID=create_userID_i)
        cla.save()

        section = Section(section=classes+' 1', classes=cla, program=program_i, sub_school=sub_school_i, school=school_i, create_userID = create_userID_i)
        section.save()

        return CreateClasses(classes=cla)

class UpdateClasses(graphene.Mutation):
    classes = graphene.Field(ClassesType)

    class Arguments:
        classes = graphene.String()
        classes_mgl = graphene.String()
        classes_numeric = graphene.String()
        degree = graphene.Int()
        activity = graphene.Int()
        max_student_num = graphene.Int()
        teacher = graphene.Int()
        program = graphene.Int()
        sub_school = graphene.Int()
        school = graphene.Int()
        status = graphene.String()
        course = graphene.String()
        end_course = graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('classes.change_classes')
    def mutate(self, info, classes, classes_mgl, classes_numeric, degree, activity, max_student_num, teacher, program, sub_school, school, status, course, end_course, id):
        
        classes_o = Classes.objects.get(pk=id)
        degree_i = Degree.objects.get(pk=degree)
        activity_i = Activity.objects.get(pk=activity)
        teacher_i = Teacher.objects.get(pk=teacher)
        program_i = Program.objects.get(pk=program)
        sub_school_i = Sub_school.objects.get(pk=sub_school)
        school_i = School.objects.get(pk=school)

        classes_o.classes = classes
        classes_o.classes_mgl = classes_mgl
        classes_o.classes_numeric = classes_numeric
        classes_o.degree = degree_i
        classes_o.activity = activity_i
        classes_o.max_student_num = max_student_num
        classes_o.teacher = teacher_i
        classes_o.program = program_i
        classes_o.sub_school = sub_school_i
        classes_o.school = school_i
        classes_o.status = status
        classes_o.course = course
        classes_o.end_course = end_course
        classes_o.save()
        return UpdateClasses(classes=classes_o)
        
class DeleteClasses(graphene.Mutation):
    classes = graphene.Field(ClassesType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('classes.delete_classes')
    def mutate(self, info, **kwargs):
        classes = Classes.objects.get(pk=kwargs["id"])
        if classes is not None:
            classes.delete()
        return DeleteClasses(classes=classes)

class Mutation(graphene.ObjectType):
    create_classes = CreateClasses.Field()
    update_classes = UpdateClasses.Field()
    delete_classes = DeleteClasses.Field()