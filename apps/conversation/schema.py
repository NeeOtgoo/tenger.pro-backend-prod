import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from graphene_file_upload.scalars import Upload
from django.db.models import Q
from .models import Conversation, ConversationFile, ConversationReply, ConversationReplyFile

class ConversationType(DjangoObjectType):
    class Meta:
        model = Conversation

class ConversationFileType(DjangoObjectType):
    class Meta:
        model = ConversationFile

class ConversationReplyType(DjangoObjectType):
    class Meta:
        model = ConversationReply

class ConversationReplyFileType(DjangoObjectType):
    class Meta:
        model = ConversationReplyFile

class ConversationDeleteType(graphene.Enum):
    sender = 0
    recipient = 1

class Query(object):
    my_inbox = graphene.List(ConversationType, filter=graphene.String(required=False, default_value=''))
    my_sent = graphene.List(ConversationType, filter=graphene.String(required=False, default_value=''))
    conversation_by_id = graphene.Field(ConversationType, id=graphene.ID(required=True))
    all_conversation_files = graphene.List(ConversationFileType, conversation=graphene.ID(required=True))
    all_conversation_reply = graphene.List(ConversationReplyType, conversation=graphene.ID(required=True))
    all_conversation_reply_files = graphene.List(ConversationReplyFileType, conversation_reply=graphene.ID(required=True))

    @login_required
    def resolve_my_inbox(self, info, filter):
        fields = Conversation.filter_fields()

        Qr = None
        for field in fields:
            q = Q(**{"%s__icontains" % field: filter })
            if Qr:
                Qr = Qr | q
            else:
                Qr = q
                
        return Conversation.objects.filter(Q(recipient=info.context.user), Q(is_recipient_deleted=False), Qr).order_by('-created_at')
    
    @login_required
    def resolve_my_sent(self, info, filter):
        fields = Conversation.filter_fields()

        Qr = None
        for field in fields:
            q = Q(**{"%s__icontains" % field: filter })
            if Qr:
                Qr = Qr | q
            else:
                Qr = q

        return Conversation.objects.filter(Q(sender=info.context.user), Q(is_sender_deleted=False), Qr).order_by('-created_at')

    @login_required
    def resolve_conversation_by_id(self, info, id):
        return Conversation.objects.get(pk=id)

    @login_required
    def resolve_all_conversation_reply(self, info, conversation):
        conversation_o = Conversation.objects.get(pk=conversation)
        return ConversationReply.objects.filter(conversation=conversation_o)

    @login_required
    def resolve_all_conversation_files(self, info, conversation):
        conversation_o = Conversation.objects.get(pk=conversation)
        return ConversationFile.objects.filter(conversation=conversation_o)

    @login_required
    def resolve_all_conversation_reply_files(self, info, conversation_reply):
        conversation_reply_o = ConversationReply.objects.get(pk=conversation_reply)
        return ConversationReplyFile.objects.filter(conversation_reply=conversation_reply_o)

class CreateConversation(graphene.Mutation):
    conversation = graphene.Field(ConversationType)

    class Arguments:
        subject = graphene.String()
        body = graphene.String()
        recipient = graphene.Int()
        groups = graphene.List(graphene.Int)
        files = graphene.List(Upload)

    @login_required
    def mutate(self, info, subject, body, recipient, groups, files):

        sender_o = get_user_model().objects.get(pk=info.context.user.pk)

        if (recipient!=0):

            recipient_o = get_user_model().objects.get(pk=recipient)
            conversation_o = Conversation(subject=subject, body=body, recipient=recipient_o, sender=sender_o)
            conversation_o.save()

            for file in files:
                file_o = ConversationFile(conversation=conversation_o, file= file['originFileObj'])
                file_o.save()

            return CreateConversation(conversation=conversation_o)

        else:
            for group in groups:
                group_o = Group.objects.get(id=group)
                users = group_o.user_set.all()
                for user in users:
                    recipient_o = get_user_model().objects.get(pk=user.pk)
                    conversation_o = Conversation(subject=subject, body=body, recipient=recipient_o, sender=sender_o)
                    conversation_o.save()
                    
                    for file in files:
                        file_o = ConversationFile(conversation=conversation_o, file= file['originFileObj'])
                        file_o.save()
                        
                return CreateConversation(conversation=conversation_o)

class DeleteConversation(graphene.Mutation):
    conversation = graphene.Field(ConversationType)

    class Arguments:
        id = graphene.ID()
        delete_type = graphene.Argument(ConversationDeleteType)

    @login_required
    def mutate(self, info, id, delete_type):

        conversation_o = Conversation.objects.get(pk=id)

        if delete_type == 0:
            conversation_o.is_sender_deleted = True
            conversation_o.save()
            return DeleteConversation(conversation=conversation_o)
        else:
            conversation_o.is_recipient_deleted = True
            conversation_o.save()
            return DeleteConversation(conversation=conversation_o)

class CreateConversationReply(graphene.Mutation):
    conversation_reply = graphene.Field(ConversationReplyType)

    class Arguments:
        conversation = graphene.ID()
        body = graphene.String()
        files = graphene.List(Upload)

    @login_required
    def mutate(self, info, conversation, body, files):

        conversation_o = Conversation.objects.get(pk=conversation)
        user_o = get_user_model().objects.get(pk=info.context.user.pk)

        conversation_reply_o = ConversationReply(conversation=conversation_o, user=user_o, body=body)
        conversation_reply_o.save()

        for file in files:
            file_o = ConversationReplyFile(conversation_reply=conversation_reply_o, file= file['originFileObj'])
            file_o.save()

        return CreateConversationReply(conversation_reply=conversation_reply_o)

class Mutation(graphene.ObjectType):
    create_conversation = CreateConversation.Field()
    delete_conversation = DeleteConversation.Field()
    create_conversation_reply = CreateConversationReply.Field()