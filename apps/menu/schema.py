import graphene
from graphene_django.types import DjangoObjectType
from .models import Menu
from django.contrib.auth.models import Permission
from graphql_jwt.decorators import login_required
from django.core import serializers

# class Menutest(graphene.Interface):
#     key =  graphene.String()
#     path = graphene.String()
#     title = graphene.String()
#     icon = graphene.String()
#     breadcrumb = graphene.String()
#     submenu = graphene.List(Menu)
#     status = graphene.String()
#     priority = graphene.String()

class MenuType(DjangoObjectType):
    class Meta:
        model = Menu
    sub_menu = graphene.JSONString()

class Query(object):
    all_menus = graphene.List(MenuType)
    # all_sub_menus = graphene.List(MenuType, id=graphene.Int(required=True))

    @login_required
    def resolve_all_menus(self, info, **kwargs):
        r = []
        
        if info.context.user.is_superuser:
            for m in Menu.objects.filter(submenu__isnull=True).order_by('priority'):

                sub = Menu.objects.filter(submenu_id=m.id,submenu__isnull=False).order_by('priority')
                m.sub_menu = serializers.serialize('json', sub)
                r.append(m)

            return r

        permissions = info.context.user.user_permissions.all().values('codename') | Permission.objects.filter(group__user=info.context.user).values('codename')

        for m in Menu.objects.filter(status='OPEN',key__in=permissions,submenu__isnull=True).order_by('priority'):

            sub = Menu.objects.filter(status='OPEN',key__in=permissions,submenu_id=m.id,submenu__isnull=False).order_by('priority')
            m.sub_menu =  serializers.serialize('json', sub)
            r.append(m)

        return r

    # # @login_required
    # def resolve_all_sub_menus(self, info, id):
    #     permissions = info.context.user.user_permissions.all().values('codename') | Permission.objects.filter(group__user=info.context.user).values('codename')

    #     return Menu.objects.filter(status='OPEN',key__in=permissions,submenu_id=id,submenu__isnull=False).order_by('priority')
      

class UpdateMenu(graphene.Mutation):
    menu = graphene.Field(MenuType)

    class Arguments:
        icon = graphene.String()
        breadcrumb = graphene.Boolean()
        submenu = graphene.Int()
        status = graphene.String()
        priority = graphene.Int()
        id = graphene.ID()

    @login_required
    def mutate(self, info, icon, breadcrumb, submenu, status, priority, id):
        
        submenu_i = Menu.objects.get(id=submenu)
        menu = Menu.objects.get(pk=id)
        menu.icon = icon
        menu.breadcrumb = breadcrumb
        menu.submenu = submenu_i
        menu.status = status
        menu.priority = priority
        menu.save()
        return UpdateMenu(menu=menu)

class Mutation(graphene.ObjectType):
    update_menu = UpdateMenu.Field()