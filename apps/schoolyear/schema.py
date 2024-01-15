import graphene
from graphene_django.types import DjangoObjectType
from .models import Schoolyear
from graphql_jwt.decorators import login_required, permission_required

class SchoolyearType(DjangoObjectType):
    class Meta:
        model = Schoolyear

class Query(object):
    all_schoolyears = graphene.List(SchoolyearType)
    schoolyear_by_id = graphene.Field(SchoolyearType, id=graphene.Int(required=True))

    @login_required
    @permission_required('schoolyear.view_schoolyear')
    def resolve_all_schoolyears(self, info, **kwargs):
        return Schoolyear.objects.all()

    @login_required
    @permission_required('schoolyear.view_schoolyear')
    def resolve_schoolyear_by_id(root, info, id):
        try:
            return Schoolyear.objects.get(id=id)
        except Schoolyear.DoesNotExist:
            return None

#******************* 😎 Schoolyear-MUTATIONS 😎 *************************#

class CreateSchoolyear(graphene.Mutation):
    schoolyear = graphene.Field(SchoolyearType)

    class Arguments:
        schoolyear = graphene.String()
        season = graphene.String()
        semester_code = graphene.String()
        start_date = graphene.String()
        end_date = graphene.String()
        is_current = graphene.Boolean()

    @login_required
    @permission_required('schoolyear.add_schoolyear')
    def mutate(self, info, schoolyear, season, semester_code, start_date, end_date, is_current):

        create_userID_i = info.context.user

        schoolyear = Schoolyear(schoolyear=schoolyear,season=season,semester_code=semester_code,start_date=start_date,end_date=end_date, is_current=is_current, create_userID=create_userID_i)
        schoolyear.save()

        if is_current == True:
            Schoolyear.objects.exclude(pk=schoolyear.pk).update(is_current=False)

        return CreateSchoolyear(schoolyear=schoolyear)

class UpdateSchoolyear(graphene.Mutation):
    schoolyear = graphene.Field(SchoolyearType)

    class Arguments:
        schoolyear = graphene.String()
        season = graphene.String()
        semester_code = graphene.String()
        start_date = graphene.String()
        end_date = graphene.String()
        is_current = graphene.Boolean()
        id = graphene.ID()

    @login_required
    @permission_required('schoolyear.change_schoolyear')
    def mutate(self, info, **kwargs):

        schoolyear = Schoolyear.objects.get(pk=kwargs["id"])

        schoolyear.schoolyear = kwargs["schoolyear"]
        schoolyear.season = kwargs["season"]
        schoolyear.semester_code = kwargs["semester_code"]
        schoolyear.start_date = kwargs["start_date"]
        schoolyear.end_date = kwargs["end_date"]
        schoolyear.is_current = kwargs["is_current"]
        schoolyear.save()

        if kwargs["is_current"] == True:
            Schoolyear.objects.exclude(pk=schoolyear.pk).update(is_current=False)

        return UpdateSchoolyear(schoolyear=schoolyear)

class DeleteSchoolyear(graphene.Mutation):
    schoolyear = graphene.Field(SchoolyearType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('schoolyear.delete_schoolyear')
    def mutate(self, info, **kwargs):
        schoolyear = Schoolyear.objects.get(pk=kwargs["id"])
        if schoolyear is not None:
            schoolyear.delete()
        return DeleteSchoolyear(schoolyear=schoolyear)

class Mutation(graphene.ObjectType):
    create_schoolyear = CreateSchoolyear.Field()
    update_schoolyear = UpdateSchoolyear.Field()
    delete_schoolyear = DeleteSchoolyear.Field()