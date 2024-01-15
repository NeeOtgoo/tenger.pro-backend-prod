import graphene
from graphene_django.types import DjangoObjectType
from .models import Event, Event_type
from datetime import datetime, timedelta
from graphql_jwt.decorators import login_required, permission_required

class EventType(DjangoObjectType):
    class Meta:
        model = Event

class Event_typeType(DjangoObjectType):
    class Meta:
        model = Event_type

class Query(object):
    all_events = graphene.List(EventType)
    all_events_by_date = graphene.List(EventType, date=graphene.Date(required=False, default_value=datetime.today()))
    all_events_by_type = graphene.Field(EventType, id=graphene.Int(required=True))
    all_event_types = graphene.List(Event_typeType)
    event_by_id = graphene.Field(EventType, id=graphene.Int(required=True))

    @login_required
    @permission_required('event.view_event')
    def resolve_all_events(self, info):
       return Event.objects.filter(start_at__gte=datetime.now() - timedelta(days=1)).order_by('start_at')

    @login_required
    @permission_required('event.view_event')
    def resolve_all_events_by_date(self, info, date):
        nxt_mnth = date.replace(day=28) + timedelta(days=4)
        last_date = nxt_mnth - timedelta(days=nxt_mnth.day)
        return Event.objects.filter(start_at__range=(date.replace(day=1), last_date)).order_by('start_at')

    @login_required
    @permission_required('event.view_event')
    def resolve_all_events_by_type(self, info, id):
        try:
            event_type_o = Event_type.objects.get(id=id)
            return Event.filter(event_type=event_type_o)
        except Event_type.DoesNotExist:
            return None
                
    @login_required
    @permission_required('event.view_event_type')
    def resolve_all_event_types(root, info):
        return Event_type.objects.all()


    @login_required
    @permission_required('event.view_event')
    def resolve_event_by_id(root, info, id):
        try:
            return Event.objects.get(pk=id)
        except Event.DoesNotExist:
                return None

#******************* 😎 Event-MUTATIONS 😎 *************************#
class CreateEvent(graphene.Mutation):
    event = graphene.Field(EventType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        content = graphene.String()
        start_at = graphene.String()
        end_at = graphene.String()
        event_type = graphene.Int()

    @login_required
    @permission_required('event.add_event')
    def mutate(self, info, title, description, content, start_at, end_at, event_type):
        
        event_type_i = Event_type.objects.get(pk=event_type)
        create_userID_i = info.context.user

        event = Event(title=title, description=description, content=content, start_at=start_at, end_at=end_at, event_type=event_type_i, create_userID=create_userID_i)
        event.save()
        return CreateEvent(event=event)

class UpdateEvent(graphene.Mutation):
    event = graphene.Field(EventType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        content = graphene.String()
        start_at = graphene.String()
        end_at = graphene.String()
        event_type = graphene.Int()
        id = graphene.ID()

    @login_required
    @permission_required('event.change_event')
    def mutate(self, info, title, description, content, start_at, end_at, event_type, id):
        
        event_o = Event.objects.get(pk=id)
        event_type_i = Event_type.objects.get(pk=event_type)
        
        event_o.title = title
        event_o.description = description
        event_o.content = content
        event_o.start_at = start_at
        event_o.end_at = end_at
        event_o.event_type = event_type_i
        event_o.save()
        return UpdateEvent(event=event_o)

class DeleteEvent(graphene.Mutation):
    event = graphene.Field(EventType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('event.delete_event')
    def mutate(self, info, **kwargs):
        event = Event.objects.get(pk=kwargs["id"])
        if event is not None:
            event.delete()
        return DeleteEvent(event=event)

#******************* 😎 Event_type-MUTATIONS 😎 *************************#
class CreateEvent_type(graphene.Mutation):
    event_type = graphene.Field(Event_typeType)

    class Arguments:
        name = graphene.String()
        color = graphene.String()

    @login_required
    @permission_required('event.add_event_type')
    def mutate(self, info, name, color):

        event_type = Event_type(name=name, color=color)
        event_type.save()
        return CreateEvent_type(event_type=event_type)

class UpdateEvent_type(graphene.Mutation):
    event_type = graphene.Field(Event_typeType)

    class Arguments:
        name = graphene.String()
        color = graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('event.change_event_type')
    def mutate(self, info, name, color, id):
        
        event_type = Event_type.objects.get(pk=id)

        event_type.name = name
        event_type.color = color
        event_type.save()
        return UpdateEvent_type(event_type=event_type)

class DeleteEvent_type(graphene.Mutation):
    event_type = graphene.Field(Event_typeType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('event.delete_event_type')
    def mutate(self, info, **kwargs):
        event_type = Event_type.objects.get(pk=kwargs["id"])
        if event_type is not None:
            event_type.delete()
        return DeleteEvent_type(event_type=event_type)

class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()
    create_event_type = CreateEvent_type.Field()
    update_event_type = UpdateEvent_type.Field()
    delete_event_type = DeleteEvent_type.Field()