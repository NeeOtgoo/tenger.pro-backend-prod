import graphene
from graphene_django.types import DjangoObjectType
from .models import Program
from .models import Program_subject
from apps.sub_school.models import Sub_school
from apps.school.models import School
from apps.core.models import Degree
from apps.subject.models import Subject
from apps.teacher.models import Teacher
from apps.student.models import Student
from graphql_jwt.decorators import login_required, permission_required

class ProgramType(DjangoObjectType):
    class Meta:
        model = Program

class Program_subjectType(DjangoObjectType):
    class Meta:
        model = Program_subject

class Query(object):
    all_programs = graphene.List(ProgramType)
    program_by_id = graphene.Field(ProgramType, id=graphene.Int(required=True))
    all_program_subject_by_program = graphene.List(Program_subjectType, id=graphene.Int(required=True))

    @login_required
    def resolve_all_programs(self, info):
        if info.context.user.is_superuser==True:
            return Program.objects.all()
            
        if info.context.user.is_student==True:
            student = Student.objects.get(user=info.context.user)
            return Program.objects.filter(pk=student.program_id)
        if info.context.user.is_teacher==True:
            teacher = Teacher.objects.get(user=info.context.user)
            return Program.objects.filter(sub_school=teacher.sub_school)
        else:
            # programs = Program.access_program(Teacher.objects.get(user=info.context.user))
            # return Program.objects.filter(pk__in=programs)
            return Program.objects.all()

    @login_required
    @permission_required('program.view_program_subject')
    def resolve_all_program_subject_by_program(self, info, id):
        try:
            program_o = Program.objects.get(pk=id)
            return Program_subject.objects.filter(program=program_o)
        except Program.DoesNotExist:
            return None

    @login_required
    @permission_required('program.view_program')
    def resolve_program_by_id(root, info, id):
        try:
            return Program.objects.get(id=id)
        except Program.DoesNotExist:
            return None

#******************* 😎 Program-MUTATIONS 😎 *************************#
class CreateProgram(graphene.Mutation):
    program = graphene.Field(ProgramType)

    class Arguments:
        program = graphene.String()
        program_mgl = graphene.String()
        program_numeric = graphene.String()
        degree = graphene.Int()
        max_student_num = graphene.Int()
        school = graphene.Int()
        sub_school = graphene.Int()
        status = graphene.String()

    @login_required
    @permission_required('program.add_program')
    def mutate(self, info, program, program_mgl, program_numeric, degree, max_student_num, sub_school, school, status):
        
        degree_i = Degree.objects.get(pk=degree)
        sub_school_i = Sub_school.objects.get(pk=sub_school)
        school_i = School.objects.get(pk=school)
        create_userID_i = info.context.user

        pro = Program(program=program, program_mgl=program_mgl, program_numeric=program_numeric, degree=degree_i, max_student_num=max_student_num, sub_school=sub_school_i, school=school_i, status=status, create_userID=create_userID_i)
        pro.save()
        return CreateProgram(program=pro)

class UpdateProgram(graphene.Mutation):
    program = graphene.Field(ProgramType)

    class Arguments:
        program = graphene.String()
        program_mgl = graphene.String()
        program_numeric = graphene.String()
        degree = graphene.Int()
        max_student_num = graphene.Int()
        school = graphene.Int()
        sub_school = graphene.Int()
        status = graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('program.change_program')
    def mutate(self, info, program, program_mgl, program_numeric, degree, max_student_num, sub_school, school, status, id):
        
        program_o = Program.objects.get(pk=id)
        degree_i = Degree.objects.get(pk=degree)
        sub_school_i = Sub_school.objects.get(pk=sub_school)
        school_i = School.objects.get(pk=school)
        
        program_o.program = program
        program_o.program_mgl = program_mgl
        program_o.program_numeric = program_numeric
        program_o.degree = degree_i
        program_o.max_student_num = max_student_num
        program_o.sub_school = sub_school_i
        program_o.school = school_i
        program_o.status = status
        program_o.save()
        return UpdateProgram(program=program_o)

class DeleteProgram(graphene.Mutation):
    program = graphene.Field(ProgramType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('program.delete_program')
    def mutate(self, info, **kwargs):
        program = Program.objects.get(pk=kwargs["id"])
        if program is not None:
            program.delete()
        return DeleteProgram(program=program)

#******************* 😎 Program_subject-MUTATIONS 😎 *************************#
class CreateProgram_subject(graphene.Mutation):
    program_subject = graphene.Field(Program_subjectType)

    class Arguments:
        program = graphene.Int()
        subject = graphene.Int()

    @login_required
    @permission_required('program.add_program_subject')
    def mutate(self, info, program, subject):
        
        program_i = Program.objects.get(pk=program)
        subject_i = Subject.objects.get(pk=subject)

        pros = Program_subject(program=program_i, subject=subject_i)
        pros.save()
        return CreateProgram_subject(program_subject=pros)

class DeleteProgram_subject(graphene.Mutation):
    program_subject = graphene.Field(Program_subjectType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('program.delete_program_subject')
    def mutate(self, info, **kwargs):
        program_subject_o = Program_subject.objects.get(pk=kwargs["id"])
        if program_subject_o is not None:
            program_subject_o.delete()
        return DeleteProgram_subject(program_subject=program_subject_o)

class Mutation(graphene.ObjectType):
    create_program = CreateProgram.Field()
    update_program = UpdateProgram.Field()
    delete_program = DeleteProgram.Field()
    create_program_subject = CreateProgram_subject.Field()
    delete_program_subject = DeleteProgram_subject.Field()