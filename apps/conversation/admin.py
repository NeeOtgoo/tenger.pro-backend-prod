from django.contrib import admin
from .models import Conversation, ConversationFile, ConversationReply

# Register your models here.

admin.site.register(Conversation)
admin.site.register(ConversationFile)
admin.site.register(ConversationReply)