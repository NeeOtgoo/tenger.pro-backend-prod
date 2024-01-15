import graphene
from graphene_django.types import DjangoObjectType
from .models import School
from graphql_jwt.decorators import login_required, permission_required

class SchoolType(DjangoObjectType):
    class Meta:
        model = School

class Query(object):
    all_schools = graphene.List(SchoolType)
    school_by_id = graphene.Field(SchoolType, id=graphene.Int(required=True))

    @login_required
    def resolve_all_schools(self, info, **kwargs):
        return School.objects.all()

    @login_required
    @permission_required('school.view_school')
    def resolve_school_by_id(root, info, id):
        try:
            return School.objects.get(id=id)
        except School.DoesNotExist:
            return None

#******************* 😎 School-MUTATIONS 😎 *************************#
class CreateSchool(graphene.Mutation):
    school = graphene.Field(SchoolType)

    class Arguments:
        name = graphene.String()
        name_mgl = graphene.String()

    @login_required
    @permission_required('school.add_school')
    def mutate(self, info, name, name_mgl):
        stu = School(name=name, name_mgl=name_mgl)
        stu.save()
        return CreateSchool(school=stu)

class UpdateSchool(graphene.Mutation):
    school = graphene.Field(SchoolType)

    class Arguments:
        name = graphene.String()
        name_mgl = graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('school.change_school')
    def mutate(self, info, name, name_mgl, id):
        school = School.objects.get(pk=id)
        school.name = name
        school.name_mgl = name_mgl
        school.save()
        return UpdateSchool(school=school)     

class DeleteSchool(graphene.Mutation):
    school = graphene.Field(SchoolType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('school.delete_school')
    def mutate(self, info, **kwargs):
        school = School.objects.get(pk=kwargs["id"])
        if school is not None:
            school.delete()
        return DeleteSchool(school=school)

class Mutation(graphene.ObjectType):
    create_school = CreateSchool.Field()
    update_school = UpdateSchool.Field()
    delete_school = DeleteSchool.Field()