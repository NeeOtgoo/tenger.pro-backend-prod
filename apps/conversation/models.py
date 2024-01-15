from django.db.models import Model, CharField, TextField, ForeignKey, CASCADE, BooleanField, FileField, DateTimeField
from django.conf import settings

class Conversation(Model):
    sender = ForeignKey(settings.AUTH_USER_MODEL, related_name = 'sender_userID', on_delete=CASCADE)
    recipient = ForeignKey(settings.AUTH_USER_MODEL, related_name = 'recipient_userID', on_delete=CASCADE)
    subject = CharField(max_length=100)
    body = TextField(blank=True)
    is_recipient_deleted = BooleanField(default=False)
    is_sender_deleted = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

    def filter_fields():
        return ['recipient__first_name','recipient__last_name','subject']

class ConversationFile(Model):
    upload_path = 'default'
    conversation = ForeignKey(Conversation, on_delete=CASCADE)
    file = FileField(upload_to='static/uploads/'+upload_path+'/conversation/%Y/%m/%d/', max_length=500)

class ConversationReply(Model):
    conversation = ForeignKey(Conversation, on_delete=CASCADE)
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    body = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)

class ConversationReplyFile(Model):
    upload_path = 'default'
    conversation_reply = ForeignKey(ConversationReply, on_delete=CASCADE)
    file = FileField(upload_to='static/uploads/'+upload_path+'/conversation-reply/%Y/%m/%d/', max_length=500)
