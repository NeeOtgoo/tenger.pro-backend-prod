import graphene
from graphene_django.types import DjangoObjectType
from .models import CustomUser
from apps.student.models import Student
from apps.teacher.models import Teacher
from apps.parent.models import Parent
from apps.employee.models import Employee
from graphql_jwt.decorators import login_required

class AccountType(DjangoObjectType):
    class Meta:
        model = CustomUser

class Custom_accountType(graphene.ObjectType):
    email = graphene.String()
    family_name = graphene.String()
    name = graphene.String()
    phone = graphene.String()
    phone2 = graphene.String()
    address = graphene.String()

class Query(object):
    all_accounts = graphene.List(AccountType)
    account_self = graphene.Field(Custom_accountType)

    @login_required
    def resolve_all_accounts(self, info, **kwargs):
        return CustomUser.objects.filter(is_student = False, is_teacher = False, is_parent = False)

    @login_required
    def resolve_account_self(self, info, **kwargs):

        user_i = info.context.user

        if user_i.is_superuser == True:
            return {
            "email":user_i.email,
            "family_name":user_i.first_name,
            "name": user_i.last_name,
            "phone": '',
            "phone2": '',
            "address": '',}
        elif user_i.is_student == True:
            account_i = Student.objects.get(pk=user_i.student.id)
        elif user_i.is_teacher == True:
            account_i = Teacher.objects.get(pk=user_i.teacher.id)
        elif user_i.is_parent == True:
            account_i = Parent.objects.get(pk=user_i.parent.id)
        elif user_i.is_employee == True:
            account_i = Employee.objects.get(pk=user_i.employee.id)

        return {
        "email":user_i.email,
        "family_name":user_i.first_name,
        "name": user_i.last_name,
        "phone": account_i.phone,
        "phone2": account_i.phone2,
        "address": account_i.address,
        }


#******************* 😎 Account-MUTATIONS 😎 *************************#
class UpdateMyAccount(graphene.Mutation):
    account = graphene.Field(Custom_accountType)

    class Arguments:
        email = graphene.String()
        family_name = graphene.String()
        name = graphene.String()
        phone = graphene.String()
        phone2 = graphene.String()
        address = graphene.String()

    @login_required
    def mutate(self, info, email, family_name, name, phone, phone2, address):

        user_i = info.context.user
        user_i.email = email
        user_i.first_name = family_name
        user_i.last_name = name
        user_i.save()

        if user_i.is_superuser == True:
            return UpdateMyAccount(account={
            "email":user_i.email,
            "family_name":user_i.first_name,
            "name": user_i.last_name,
            "phone": '',
            "phone2": '',
            "address": '',})
        elif user_i.is_student == True:
            account_i = Student.objects.get(pk=user_i.student.id)
        elif user_i.is_teacher == True:
            account_i = Teacher.objects.get(pk=user_i.teacher.id)
        elif user_i.is_parent == True:
            account_i = Parent.objects.get(pk=user_i.parent.id)
        elif user_i.is_employee == True:
            account_i = Employee.objects.get(pk=user_i.employee.id)
        
        account_i.family_name = family_name
        account_i.name = name
        account_i.phone = phone
        account_i.phone2 = phone2
        account_i.address = address
        account_i.save()
        return UpdateMyAccount(account=account_i)

class Mutation(graphene.ObjectType):
    update_my_account = UpdateMyAccount.Field()