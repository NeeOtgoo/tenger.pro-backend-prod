import graphene
from graphene_django.types import DjangoObjectType
from .models import Sub_school
from apps.school.models import School
from graphql_jwt.decorators import login_required, permission_required

class SubSchoolType(DjangoObjectType):
    class Meta:
        model = Sub_school

class Query(object):
    all_sub_schools = graphene.List(SubSchoolType)
    sub_school_by_id = graphene.Field(SubSchoolType, id=graphene.Int(required=True))

    @login_required
    def resolve_all_sub_schools(self, info, **kwargs):
        return Sub_school.objects.all()

    @login_required
    @permission_required('sub_school.view_sub_school')
    def resolve_sub_school_by_id(root, info, id):
        try:
            return Sub_school.objects.get(id=id)
        except Sub_school.DoesNotExist:
            return None

#******************* 😎 Sub_school-MUTATIONS 😎 *************************#
class CreateSub_school(graphene.Mutation):
    sub_school = graphene.Field(SubSchoolType)

    class Arguments:
        name = graphene.String()
        name_mgl = graphene.String()
        school = graphene.Int()

    @login_required
    def mutate(self, info, name, name_mgl, school):
        
        school_i = School.objects.get(pk=school)

        stu = Sub_school(name=name, name_mgl=name_mgl, school=school_i)
        stu.save()
        return CreateSub_school(sub_school=stu)

class UpdateSub_school(graphene.Mutation):
    sub_school = graphene.Field(SubSchoolType)

    class Arguments:
        name = graphene.String()
        name_mgl = graphene.String()
        school = graphene.Int()
        id = graphene.ID()

    @login_required
    @permission_required('sub_school.change_sub_school')
    def mutate(self, info, name, name_mgl, school, id):
        
        sub_school_o = Sub_school.objects.get(pk=id)
        school_i = School.objects.get(pk=school)

        sub_school_o.name = name
        sub_school_o.name_mgl = name_mgl
        sub_school_o.school = school_i
        sub_school_o.save()
        return UpdateSub_school(sub_school=sub_school_o)

class DeleteSub_school(graphene.Mutation):
    sub_school = graphene.Field(SubSchoolType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('sub_school.delete_sub_school')
    def mutate(self, info, **kwargs):
        sub_school = Sub_school.objects.get(pk=kwargs["id"])
        if sub_school is not None:
            sub_school.delete()
        return DeleteSub_school(sub_school=sub_school)

class Mutation(graphene.ObjectType):
    create_sub_school = CreateSub_school.Field()
    update_sub_school = UpdateSub_school.Field()
    delete_sub_school = DeleteSub_school.Field()