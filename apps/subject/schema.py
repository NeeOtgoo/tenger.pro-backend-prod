import graphene
from graphene_django.types import DjangoObjectType
from .models import Subject
from apps.school.models import School
from apps.sub_school.models import Sub_school
from graphql_jwt.decorators import login_required, permission_required
from django.db.models import Q

class SubjectType(DjangoObjectType):
    class Meta:
        model = Subject

class Query(object):
    all_subjects = graphene.List(SubjectType, offset=graphene.Int(required=False, default_value=0), limit=graphene.Int(required=False, default_value=50), filter=graphene.String(required=False, default_value=''))
    subject_by_id = graphene.Field(SubjectType, id=graphene.Int(required=True))

    @login_required
    def resolve_all_subjects(self, info, offset, limit, filter):
        fields = Subject.filter_fields()

        Qr = None
        for field in fields:
            q = Q(**{"%s__icontains" % field: filter })
            if Qr:
                Qr = Qr | q
            else:
                Qr = q

        return Subject.objects.filter(Qr)

    @login_required
    @permission_required('subject.view_subject')
    def resolve_subject_by_id(self, info, id):
        return  Subject.objects.get(pk=id)

#******************* 😎 Subject-MUTATIONS 😎 *************************#
class CreateSubject(graphene.Mutation):
    subject = graphene.Field(SubjectType)

    class Arguments:
        school = graphene.Int()
        sub_school = graphene.Int()
        subject = graphene.String()
        subject_mgl = graphene.String()
        subject_code = graphene.String()
        credit = graphene.String()
        part = graphene.String()

    @login_required
    @permission_required('subject.add_subject')
    def mutate(self, info, school, sub_school, subject, subject_mgl, subject_code, credit, part):
        
        sub_school_i = Sub_school.objects.get(pk=sub_school)
        school_i = School.objects.get(pk=school)
        create_userID_i = info.context.user

        subject = Subject(school=school_i, sub_school=sub_school_i, part=part, subject=subject, subject_mgl=subject_mgl, subject_code=subject_code, credit=credit, create_userID=create_userID_i)
        subject.save()
        return CreateSubject(subject=subject)

class UpdateSubject(graphene.Mutation):
    subject = graphene.Field(SubjectType)

    class Arguments:
        school = graphene.Int()
        sub_school = graphene.Int()
        subject = graphene.String()
        subject_mgl = graphene.String()
        subject_code = graphene.String()
        credit = graphene.String()
        id = graphene.ID()
        part = graphene.String()

    @login_required
    @permission_required('subject.add_subject')
    def mutate(self, info, school, sub_school, subject, subject_mgl, subject_code, credit, id, part):
        
        subject_o = Subject.objects.get(pk=id)
        sub_school_i = Sub_school.objects.get(pk=sub_school)
        school_i = School.objects.get(pk=school)
        
        subject_o.school = school_i
        subject_o.sub_school = sub_school_i
        subject_o.subject = subject
        subject_o.subject_mgl = subject_mgl
        subject_o.subject_code = subject_code
        subject_o.credit = credit
        subject_o.part = part
        subject_o.save()
        return UpdateSubject(subject=subject_o)

class DeleteSubject(graphene.Mutation):
    subject = graphene.Field(SubjectType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('subject.delete_subject')
    def mutate(self, info, **kwargs):
        subject = Subject.objects.get(pk=kwargs["id"])
        if subject is not None:
            subject.delete()
        return DeleteSubject(subject=subject)

class Mutation(graphene.ObjectType):
    create_subject = CreateSubject.Field()
    update_subject = UpdateSubject.Field()
    delete_subject = DeleteSubject.Field()