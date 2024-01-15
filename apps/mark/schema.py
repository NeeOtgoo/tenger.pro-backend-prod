import graphene
from graphene_django.types import DjangoObjectType
from .models import Mark_board, Mark, Mark_percentage, Mark_rel, Mark_setting
from django.conf import settings
from apps.schoolyear.models import Schoolyear
from apps.subject.models import Subject
from apps.student.models import Student
from apps.teacher.models import Teacher
from apps.routine.models import Routine, Routine_student
from graphql_jwt.decorators import login_required, permission_required
from django.db.models import Sum
from django.db.models import Q

class Mark_boardType(DjangoObjectType):
    class Meta:
        model = Mark_board

class MarkType(DjangoObjectType):
    class Meta:
        model = Mark

class Mark_percentageType(DjangoObjectType):
    class Meta:
        model = Mark_percentage

class Mark_settingType(DjangoObjectType):
    class Meta:
        model = Mark_setting

class Mark_relType(DjangoObjectType):
    class Meta:
        model = Mark_rel

class Mark_subjectType(graphene.ObjectType):
    subject_id = graphene.String()
    subject = graphene.String()
    subject_code = graphene.String()
    subject_credit = graphene.String()
    percentage = graphene.String()
    type = graphene.String()
    diam = graphene.String()

class Query(object):
    all_mark_boards = graphene.List(Mark_boardType, offset=graphene.Int(required=False, default_value=0), limit=graphene.Int(required=False, default_value=50), filter=graphene.String(required=False, default_value=''))
    mark_board_by_id = graphene.Field(Mark_boardType, id=graphene.Int(required=True))
    all_marks = graphene.List(MarkType, mark_board=graphene.Int(required=True))
    all_mark_percentages = graphene.List(Mark_percentageType)
    mark_percentage_by_id = graphene.Field(Mark_percentageType, id=graphene.Int(required=True))
    all_mark_settings = graphene.List(Mark_settingType)
    mark_settings_by_part = graphene.List(Mark_settingType, part=graphene.String(required=True))
    mark_setting_by_id = graphene.Field(Mark_settingType, id=graphene.Int(required=True))
    all_mark_rels = graphene.List(Mark_relType, mark=graphene.Int(required=True))
    student_mark_subjects = graphene.List(Mark_subjectType)


    @login_required
    @permission_required('mark.view_mark_board')
    def resolve_all_mark_boards(self, info, offset, limit, filter):

        fields = Mark_board.filter_fields()

        Qr = None
        for field in fields:
            q = Q(**{"%s__icontains" % field: filter })
            if Qr:
                Qr = Qr | q
            else:
                Qr = q

        if info.context.user.is_superuser==True:
            return Mark_board.objects.filter(Qr)[offset:limit]
            
        if info.context.user.is_student==True:
            return None
        else:
            teachers = Teacher.access_teacher(Teacher.objects.get(user=info.context.user))
            return Mark_board.objects.filter(Q(teacher_id__in=teachers), Qr)[offset:limit]

    @login_required
    @permission_required('mark.view_mark_board')
    def resolve_mark_board_by_id(root, info, id):
        try:
            return Mark_board.objects.get(pk=id)
        except Mark_board.DoesNotExist:
            return None
            
    @login_required
    @permission_required('mark.view_mark')
    def resolve_all_marks(self, info, mark_board):
        return Mark.objects.filter(mark_board=mark_board)
            
    @login_required
    @permission_required('mark.view_mark_percentage')
    def resolve_all_mark_percentages(self, info, **kwargs):
        return Mark_percentage.objects.all()

    @login_required
    @permission_required('mark.view_mark_percentage')
    def resolve_mark_percentage_by_id(root, info, id):
        try:
            return Mark_percentage.objects.get(pk=id)
        except Mark_percentage.DoesNotExist:
            return None
            
    @login_required
    def resolve_all_mark_settings(self, info, **kwargs):
        return Mark_setting.objects.all()

    @login_required
    def resolve_mark_settings_by_part(self, info, part):
        return Mark_setting.objects.filter(part=part)

    @login_required
    @permission_required('mark.view_mark_setting')
    def resolve_mark_setting_by_id(root, info, id):
        try:
            return Mark_setting.objects.get(pk=id)
        except Mark_setting.DoesNotExist:
            return None

    @login_required
    @permission_required('mark.view_mark')
    def resolve_all_mark_rels(self, info, mark):
        return Mark_rel.objects.filter(mark=mark)

    @login_required
    def resolve_student_mark_subjects(root, info):
        reports = []
 
        if info.context.user.is_student==True:
            student = Student.objects.get(user=info.context.user)
            mark_boards = Mark.objects.filter(student=student).values('mark_board_id')

            subjects = Mark_board.objects.filter(pk__in=mark_boards).values('subject_id')

            for subject in Subject.objects.filter(pk__in=subjects):

                mark = Mark.objects.get(mark_board__subject_id=subject.pk, student_id=student)

                mark_val = Mark_rel.objects.filter(mark=mark, mark__student_id=student).aggregate(Sum('mark_val')).get('mark_val__sum')

                percentage_type = Mark_percentage.objects.get(percentage = mark_val)

                reports.append({
                "subject_id":subject.pk,
                "subject":subject.subject,
                "subject_code":subject.subject_code,
                "subject_credit": subject.credit,
                "percentage":str(mark_val),
                "type":percentage_type.type,
                "diam":percentage_type.diam,
                }) 

        return reports
        

#******************* 😎 Mark_board-MUTATIONS 😎 *************************#
class CreateMark_board(graphene.Mutation):
    mark_board = graphene.Field(Mark_boardType)

    class Arguments:
        schoolyear = graphene.Int()
        subject = graphene.Int()
        teacher = graphene.Int()
        start_at = graphene.String()
        end_at = graphene.String()
        status = graphene.String()

    @login_required
    @permission_required('mark.add_mark_board')
    def mutate(self, info, schoolyear, subject, teacher, start_at, end_at, status):
        
        schoolyear_i = Schoolyear.objects.get(pk=schoolyear)
        subject_i = Subject.objects.get(pk=subject)
        teacher_i = Teacher.objects.get(pk=teacher)
        create_userID_i = info.context.user

        mark_board_o = Mark_board(
            schoolyear=schoolyear_i, 
            subject=subject_i, 
            teacher=teacher_i, 
            start_at=start_at, 
            end_at=end_at, 
            status=status, 
            create_userID=create_userID_i
        )
        mark_board_o.save()
        return CreateMark_board(mark_board=mark_board_o)

class CreateMark_board_from_routine(graphene.Mutation):
    mark_board = graphene.Field(Mark_boardType)

    class Arguments:
        routine = graphene.Int()
        start_at = graphene.String()
        end_at = graphene.String()
        status = graphene.String()

    @login_required
    @permission_required('mark.add_mark_board')
    def mutate(self, info, routine, start_at, end_at, status):

        routine = Routine.objects.get(pk=routine)
        create_userID_i = info.context.user

        mark_board_o = Mark_board(
            schoolyear=routine.schoolyear, 
            subject=routine.subject, 
            teacher=routine.teacher, 
            start_at=start_at, 
            end_at=end_at, 
            status=status,
            create_userID=create_userID_i
        )
        mark_board_o.save()

        mark_board_inserted = Mark_board.objects.latest('id')

        for student in Routine_student.objects.filter(routine=routine):

            mark = Mark(mark_board=mark_board_inserted, student=student, create_userID=create_userID_i)
            mark.save()

        return CreateMark_board_from_routine(mark_board=mark_board_o)

class UpdateMark_board(graphene.Mutation):
    mark_board = graphene.Field(Mark_boardType)

    class Arguments:
        schoolyear = graphene.Int()
        subject = graphene.Int()
        teacher = graphene.Int()
        start_at = graphene.String()
        end_at = graphene.String()
        status = graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('mark.change_mark_board')
    def mutate(self, info, schoolyear, subject, teacher, start_at, end_at, status, id):
        
        mark_board_o = Mark_board.objects.get(pk=id)
        schoolyear_i = Schoolyear.objects.get(pk=schoolyear)
        subject_i = Subject.objects.get(pk=subject)
        teacher_i = Teacher.objects.get(pk=teacher)

        mark_board_o.schoolyear = schoolyear_i
        mark_board_o.subject = subject_i
        mark_board_o.teacher = teacher_i
        mark_board_o.start_at = start_at
        mark_board_o.end_at = end_at
        mark_board_o.status = status
        mark_board_o.save()
        return UpdateMark_board(mark_board=mark_board_o)
        
class DeleteMark_board(graphene.Mutation):
    mark_board = graphene.Field(Mark_boardType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('mark.delete_mark_board')
    def mutate(self, info, **kwargs):
        mark_board_o = Mark_board.objects.get(pk=kwargs["id"])
        if mark_board_o is not None:
            mark_board_o.delete()
        return DeleteMark_board(mark_board=mark_board_o)

#******************* 😎 Mark-MUTATIONS 😎 *************************#
class CreateMark(graphene.Mutation):
    mark = graphene.Field(MarkType)

    class Arguments:
        mark_board = graphene.Int()
        student_code = graphene.String()
        section = graphene.Int()

    @login_required
    @permission_required('mark.add_mark')
    def mutate(self, info, mark_board, student_code = '', section = 0):
        mark_board_i = Mark_board.objects.get(pk=mark_board)

        mark = None

        if student_code=='' and section > 0:
            for student in Student.objects.filter(section=section):
                try:
                    mark = Mark.objects.get(mark_board=mark_board_i, student=student)
                except Mark.DoesNotExist:
                    mark = Mark(mark_board=mark_board_i, student=student, create_userID=info.context.user)
                    mark.save()
        elif student_code!='' and section == 0:
            student = Student.objects.get(student_code=student_code)
            try:
                mark = Mark.objects.get(mark_board=mark_board_i, student=student)
            except Mark.DoesNotExist:
                mark = Mark(mark_board=mark_board_i, student=student, create_userID=info.context.user)
                mark.save()
            
        return CreateMark(mark=mark)
        
class DeleteMark(graphene.Mutation):
    mark = graphene.Field(MarkType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('mark.delete_mark')
    def mutate(self, info, **kwargs):
        mark = Mark.objects.get(pk=kwargs["id"])
        if mark is not None:
            mark.delete()
        return DeleteMark(mark=mark)

#******************* 😎 Mark_percentage-MUTATIONS 😎 *************************#
class CreateMark_percentage(graphene.Mutation):
    mark_percentage = graphene.Field(Mark_percentageType)

    class Arguments:
        type = graphene.String()
        percentage = graphene.Int()
        diam = graphene.String()

    @login_required
    @permission_required('mark.add_mark_percentage')
    def mutate(self, info, type, percentage, diam):
        
        create_userID_i = info.context.user

        mark_percentage_o = Mark_percentage(type=type, percentage=percentage, diam=diam, create_userID=create_userID_i)
        mark_percentage_o.save()
        return CreateMark_percentage(mark_percentage=mark_percentage_o)

class UpdateMark_percentage(graphene.Mutation):
    mark_percentage = graphene.Field(Mark_percentageType)

    class Arguments:
        type = graphene.String()
        percentage = graphene.Int()
        diam = graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('mark.change_mark_percentage')
    def mutate(self, info, type, percentage, diam, id):
        
        mark_percentage = Mark_percentage.objects.get(pk=id)

        mark_percentage.type = type
        mark_percentage.percentage = percentage
        mark_percentage.diam = diam
        mark_percentage.save()
        return UpdateMark_percentage(mark_percentage=mark_percentage)
        
class DeleteMark_percentage(graphene.Mutation):
    mark_percentage = graphene.Field(Mark_percentageType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('mark.delete_mark_percentage')
    def mutate(self, info, **kwargs):
        mark_percentage = Mark_percentage.objects.get(pk=kwargs["id"])
        if mark_percentage is not None:
            mark_percentage.delete()
        return DeleteMark_percentage(mark_percentage=mark_percentage)     

#******************* 😎 Mark_setting-MUTATIONS 😎 *************************#
class CreateMark_setting(graphene.Mutation):
    mark_setting = graphene.Field(Mark_settingType)

    class Arguments:
        name = graphene.String()
        percentage = graphene.Int()
        part = graphene.String()
        pass_val = graphene.Int()

    @login_required
    @permission_required('mark.add_mark_setting')
    def mutate(self, info, name, percentage, part, pass_val):
        
        create_userID_i = info.context.user

        mark_setting = Mark_setting(name=name, percentage=percentage, part=part, pass_val=pass_val, create_userID=create_userID_i)
        mark_setting.save()
        return CreateMark_setting(mark_setting=mark_setting)

class UpdateMark_setting(graphene.Mutation):
    mark_setting = graphene.Field(Mark_settingType)

    class Arguments:
        name = graphene.String()
        percentage = graphene.Int()
        part = graphene.String()
        pass_val = graphene.Int()
        id = graphene.ID()

    @login_required
    @permission_required('mark.change_mark_setting')
    def mutate(self, info, name, percentage, id, part, pass_val):
        
        mark_setting = Mark_setting.objects.get(pk=id)

        mark_setting.name = name
        mark_setting.percentage = percentage
        mark_setting.part = part
        mark_setting.pass_val = pass_val
        mark_setting.save()
        return UpdateMark_setting(mark_setting=mark_setting)
        
class DeleteMark_setting(graphene.Mutation):
    mark_setting = graphene.Field(Mark_settingType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('mark.delete_mark_setting')
    def mutate(self, info, **kwargs):
        mark_setting = Mark_setting.objects.get(pk=kwargs["id"])
        if mark_setting is not None:
            mark_setting.delete()
        return DeleteMark_setting(mark_setting=mark_setting)

#******************* 😎 Mark_rel-MUTATIONS 😎 *************************#
class CreateMark_rel(graphene.Mutation):
    mark_rel = graphene.Field(Mark_relType)

    class Arguments:
        mark = graphene.Int()
        mark_setting = graphene.Int()
        mark_val = graphene.String()

    @login_required
    @permission_required('mark.add_mark_rel')
    def mutate(self, info, mark, mark_setting, mark_val):
        
        mark_i = Mark.objects.get(pk=mark)
        mark_setting_i = Mark_setting.objects.get(pk=mark_setting)
        
        mark_rel_old = Mark_rel.objects.filter(mark=mark, mark_setting=mark_setting)
        if mark_rel_old is not None:
            mark_rel_old.delete()

        mark_rel_o = Mark_rel(mark=mark_i, mark_setting=mark_setting_i, mark_val=mark_val)
        mark_rel_o.save()
        return CreateMark_rel(mark_rel=mark_rel_o)
        
class DeleteMark_rel(graphene.Mutation):
    mark_rel = graphene.Field(Mark_relType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('mark.delete_mark_rel')
    def mutate(self, info, **kwargs):
        mark_rel = Mark_rel.objects.get(pk=kwargs["id"])
        if mark_rel is not None:
            mark_rel.delete()
        return DeleteMark_rel(mark_rel=mark_rel)

class Mutation(graphene.ObjectType):
    create_mark_board_from_routine = CreateMark_board_from_routine.Field()
    create_mark_board = CreateMark_board.Field()
    update_mark_board = UpdateMark_board.Field()
    delete_mark_board = DeleteMark_board.Field()
    create_mark = CreateMark.Field()
    delete_mark = DeleteMark.Field()
    create_mark_percentage = CreateMark_percentage.Field()
    update_mark_percentage = UpdateMark_percentage.Field()
    delete_mark_percentage = DeleteMark_percentage.Field()
    create_mark_setting = CreateMark_setting.Field()
    update_mark_setting = UpdateMark_setting.Field()
    delete_mark_setting = DeleteMark_setting.Field()
    create_mark_rel = CreateMark_rel.Field()
    delete_mark_rel = DeleteMark_rel.Field()