import graphene
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from .models import Parent
from apps.student.models import Student
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from graphql_jwt.decorators import login_required, permission_required
from django.db.models import Q

class ParentType(DjangoObjectType):
    class Meta:
        model = Parent

class Query(object):
    all_parents = graphene.List(ParentType, offset=graphene.Int(required=False, default_value=0), limit=graphene.Int(required=False, default_value=50), filter=graphene.String(required=False, default_value=''))
    parent_by_id = graphene.Field(ParentType, id=graphene.Int(required=True))

    @login_required
    @permission_required('parent.view_parent')
    def resolve_all_parents(self, info, offset, limit, filter):

        fields = Parent.filter_fields()

        Qr = None
        for field in fields:
            q = Q(**{"%s__icontains" % field: filter })
            if Qr:
                Qr = Qr | q
            else:
                Qr = q

        return Parent.objects.filter(Qr)[offset:limit]

    @login_required
    @permission_required('parent.view_parent')
    def resolve_parent_by_id(self, info, id):
        return Parent.objects.filter(pk=id)

#******************* 😎 Parent-MUTATIONS 😎 *************************#
class CreateParent(graphene.Mutation):
    parent = graphene.Field(ParentType)

    class Arguments:
        family_name = graphene.String()
        name = graphene.String()
#        photo = Upload(required=True)
        profession = graphene.String()
        phone = graphene.String()
        address = graphene.String()
        address_live = graphene.String()
        student = graphene.Int()

        password = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    @login_required
    @permission_required('parent.add_parent')
    def mutate(self, info, family_name, name, profession, phone, address, address_live, student, password, username, email):
        
        student_i = Student.objects.get(pk=student)
        create_userID_i = info.context.user

        userob = get_user_model()(username=username,email=email,first_name=family_name,last_name=name,is_student=False,is_teacher=False,is_parent=True)
        userob.set_password(password)
        userob.save()
        user_i = get_user_model().objects.get(pk=userob.pk)

        
        group = Group.objects.get(pk=3)
        group.user_set.add(user_i)

        parent = Parent(user=user_i, family_name=family_name, name=name, profession=profession, phone=phone, address=address, address_live=address_live, student=student_i, create_userID=create_userID_i)
        parent.save()
        return CreateParent(parent=parent)

class UpdateParent(graphene.Mutation):
    parent = graphene.Field(ParentType)

    class Arguments:
        family_name = graphene.String()
        name = graphene.String()
#        photo = Upload(required=True)
        profession = graphene.String()
        phone = graphene.String()
        address = graphene.String()
        address_live = graphene.String()
        student = graphene.Int()
        id = graphene.ID()

    @login_required
    @permission_required('parent.change_parent')
    def mutate(self, info, family_name, name, profession, phone, address, address_live, student, id):
        
        parent = Parent.objects.get(pk=id)
        student_i = Student.objects.get(pk=student)
        
        parent.family_name = family_name
        parent.name = name
        parent.profession = profession
        parent.phone = phone
        parent.address = address
        parent.address_live = address_live
        parent.student = student_i
        parent.save()
        return UpdateParent(parent=parent)

class DeleteParent(graphene.Mutation):
    parent = graphene.Field(ParentType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('parent.delete_parent')
    def mutate(self, info, **kwargs):
        parent = Parent.objects.get(pk=kwargs["id"])
        if parent is not None:
            userob = get_user_model()(pk = parent.user_id)
            userob.delete()
            parent.delete()
        return DeleteParent(parent=parent)

class Mutation(graphene.ObjectType):
    create_parent = CreateParent.Field()
    update_parent = UpdateParent.Field()
    delete_parent = DeleteParent.Field()