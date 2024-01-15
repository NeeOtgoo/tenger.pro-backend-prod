from turtle import title
import graphene
from graphene_django.types import DjangoObjectType
from .models import Support, SupportFile, SupportGroup
from django.contrib.auth.models import Group
from graphql_jwt.decorators import login_required, permission_required
from graphene_file_upload.scalars import Upload
from django.db.models import Q

class SupportType(DjangoObjectType):
    class Meta:
        model = Support

class SupportFileType(DjangoObjectType):
    class Meta:
        model = SupportFile

class SupportGroupType(DjangoObjectType):
    class Meta:
        model = SupportGroup

class Query(object):
    all_supports = graphene.List(SupportType)
    test = graphene.String()

    def resolve_test(self, info):
        return info.context.user.groups.first()

    @login_required
    def resolve_all_supports(self, info, **kwargs):
        if info.context.user.is_superuser==True:
            return Support.objects.all()
        else:
            return Support.objects.filter(Q(supportgroup__group=info.context.user.groups.first()))

class CreateSupport(graphene.Mutation):
    support = graphene.Field(SupportType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()

    @login_required
    @permission_required('support.add_support')
    def mutate(self, info, title, description):

        support_o = Support(title=title, description=description)
        support_o.save()

        return CreateSupport(support=support_o)

class UpdateSupport(graphene.Mutation):
    support = graphene.Field(SupportType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        id = graphene.Int()

    @login_required
    @permission_required('support.change_support')
    def mutate(self, info, title, description, id):

        support = Support.objects.get(pk=id)
        support.title = title
        support.description = description
        
        support.save()

        return UpdateSupport(support=support)

class DeleteSupport(graphene.Mutation):
    support = graphene.Field(SupportType)

    class Arguments:
        id = graphene.Int()

    @login_required
    @permission_required('support.delete_support')
    def mutate(self, info, id):

        support = Support.objects.get(pk=id)
        support.delete()

        return DeleteSupport(support=support)

class CreateSupportFile(graphene.Mutation):
    support_file = graphene.Field(SupportFileType)

    class Arguments:
        support = graphene.Int()
        file = Upload()

    @login_required
    @permission_required('support.add_supportfile')
    def mutate(self, info, support, file):

        support_o = Support.objects.get(pk=support)

        support_file = SupportFile(file=file, support=support_o)
        support_file.save()

        return CreateSupportFile(support_file=support_file)
        
class DeleteSupportFile(graphene.Mutation):
    support_file = graphene.Field(SupportFileType)

    class Arguments:
        id = graphene.Int()

    @login_required
    @permission_required('support.add_supportfile')
    def mutate(self, info, id):

        support_file = SupportFile.objects.get(pk=id)
        support_file.delete()

        return DeleteSupportFile(support_file=support_file)

class AttachOrDetachSupportGroup(graphene.Mutation):
    support_group = graphene.Field(SupportGroupType)

    class Arguments:
        support = graphene.Int()
        group = graphene.Int()

    @login_required
    @permission_required('support.add_supportgroup')

    def mutate(self, info, support, group):

        group_o = Group.objects.get(pk=group)
        support_o = Support.objects.get(pk=support)

        try:
            support_group = SupportGroup.objects.get(support=support_o, group=group_o)
            support_group.delete()
        except SupportGroup.DoesNotExist:
            support_group = SupportGroup(support=support_o, group=group_o)
            support_group.save()

        return AttachOrDetachSupportGroup(support_group=support_group)

class Mutation(graphene.ObjectType):
    create_support = CreateSupport.Field()
    update_support = UpdateSupport.Field()
    delete_support = DeleteSupport.Field()
    create_support_file = CreateSupportFile.Field()
    delete_support_file = DeleteSupportFile.Field()
    attach_or_detach_support_group = AttachOrDetachSupportGroup.Field()