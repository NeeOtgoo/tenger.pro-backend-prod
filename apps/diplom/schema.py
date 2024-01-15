import graphene
from graphene_django.types import DjangoObjectType
from apps.diplom.models import Diplom, Diplom_archive
from apps.student.models import Student
from graphql_jwt.decorators import login_required, permission_required

class DiplomType(DjangoObjectType):
    class Meta:
        model = Diplom

class Diplom_archiveType(DjangoObjectType):
    class Meta:
        model = Diplom_archive

        
class Query(object):
    all_diploms = graphene.List(DiplomType)
    diplom_by_id = graphene.Field(DiplomType, id=graphene.Int(required=True))

    @login_required
    @permission_required('diplom.view_diplom')
    def resolve_all_diploms(self, info, **kwargs):
        try:
            return Diplom.objects.all()
        except Diplom.DoesNotExist:
            return None

    @login_required
    @permission_required('diplom.view_diplom')
    def resolve_diplom_by_id(self, info, id):
        try:
            return Diplom.objects.get(pk=id)
        except Diplom.DoesNotExist:
            return None

#******************* 😎 Diplom-MUTATIONS 😎 *************************#
class CreateDiplom(graphene.Mutation):
    diplom = graphene.Field(DiplomType)

    class Arguments:
        name = graphene.String(required=True)
        main_mid = graphene.String(required=True)
        main_bottom1 = graphene.String(required=True)
        main_bottom2 = graphene.String(required=True)
        main_bottom3 = graphene.String(required=True)
        mgl_main_mid = graphene.String(required=True)
        mgl_main_bottom1 = graphene.String(required=True)
        mgl_main_bottom2 = graphene.String(required=True)
        mgl_main_bottom3 = graphene.String(required=True)
        mgl_main_bottom1_sub = graphene.String(required=True)
        mgl_main_bottom2_sub = graphene.String(required=True)
        mgl_main_bottom3_sub = graphene.String(required=True)
        mark_bottom1 = graphene.String(required=True)
        mark_bottom2 = graphene.String(required=True)
        mgl_mark_bottom1 = graphene.String(required=True)
        mgl_mark_bottom2 = graphene.String(required=True)

    @login_required
    @permission_required('diplom.add_diplom')
    def mutate(self, info, **kwargs):
        
        diplom = Diplom(
          name=kwargs["name"],
          main_mid=kwargs["main_mid"],
          main_bottom1=kwargs["main_bottom1"],
          main_bottom2=kwargs["main_bottom2"],
          main_bottom3=kwargs["main_bottom3"],
          mgl_main_mid=kwargs["mgl_main_mid"],
          mgl_main_bottom1=kwargs["mgl_main_bottom1"],
          mgl_main_bottom2=kwargs["mgl_main_bottom2"],
          mgl_main_bottom3=kwargs["mgl_main_bottom3"],
          mgl_main_bottom1_sub=kwargs["mgl_main_bottom1_sub"],
          mgl_main_bottom2_sub=kwargs["mgl_main_bottom2_sub"],
          mgl_main_bottom3_sub=kwargs["mgl_main_bottom3_sub"],
          mark_bottom1=kwargs["mark_bottom1"],
          mark_bottom2=kwargs["mark_bottom2"],
          mgl_mark_bottom1=kwargs["mgl_mark_bottom1"],
          mgl_mark_bottom2=kwargs["mgl_mark_bottom2"],
          create_userID = info.context.user
        )
        diplom.save()
        return CreateDiplom(diplom=diplom)

class UpdateDiplom(graphene.Mutation):
    diplom = graphene.Field(DiplomType)

    class Arguments:
        name = graphene.String()
        main_mid = graphene.String()
        main_bottom1 = graphene.String()
        main_bottom2 = graphene.String()
        main_bottom3 = graphene.String()
        mgl_main_mid = graphene.String()
        mgl_main_bottom1 = graphene.String()
        mgl_main_bottom2 = graphene.String()
        mgl_main_bottom3 = graphene.String()
        mgl_main_bottom1_sub = graphene.String()
        mgl_main_bottom2_sub = graphene.String()
        mgl_main_bottom3_sub = graphene.String()
        mark_bottom1 = graphene.String()
        mark_bottom2 = graphene.String()
        mgl_mark_bottom1 = graphene.String()
        mgl_mark_bottom2 = graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('diplom.change_diplom')
    def mutate(self, info, **kwargs):
        
        diplom = Diplom.objects.get(pk=kwargs["id"])

        diplom.name = kwargs["name"]
        diplom.main_mid = kwargs["main_mid"]
        diplom.main_bottom1 = kwargs["main_bottom1"]
        diplom.main_bottom2 = kwargs["main_bottom2"]
        diplom.main_bottom3 = kwargs["main_bottom3"]
        diplom.mgl_main_mid = kwargs["mgl_main_mid"]
        diplom.mgl_main_bottom1 = kwargs["mgl_main_bottom1"]
        diplom.mgl_main_bottom2 = kwargs["mgl_main_bottom2"]
        diplom.mgl_main_bottom3 = kwargs["mgl_main_bottom3"]
        diplom.mgl_main_bottom1_sub = kwargs["mgl_main_bottom1_sub"]
        diplom.mgl_main_bottom2_sub = kwargs["mgl_main_bottom2_sub"]
        diplom.mgl_main_bottom3_sub = kwargs["mgl_main_bottom3_sub"]
        diplom.mark_bottom1 = kwargs["mark_bottom1"]
        diplom.mark_bottom2 = kwargs["mark_bottom2"]
        diplom.mgl_mark_bottom1 = kwargs["mgl_mark_bottom1"]
        diplom.mgl_mark_bottom2 = kwargs["mgl_mark_bottom2"]
        diplom.create_userID = info.context.user
        diplom.save()
        return UpdateDiplom(diplom=diplom)
        
class DeleteDiplom(graphene.Mutation):
    diplom = graphene.Field(DiplomType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('diplom.delete_diplom')
    def mutate(self, info, **kwargs):
        diplom = Diplom.objects.get(pk=kwargs["id"])
        if diplom is not None:
            diplom.delete()
        return DeleteDiplom(diplom=diplom)

class Mutation(graphene.ObjectType):
    create_diplom = CreateDiplom.Field()
    update_diplom = UpdateDiplom.Field()
    delete_diplom = DeleteDiplom.Field()