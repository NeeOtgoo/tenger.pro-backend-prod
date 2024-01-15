# Generated by Django 3.2.15 on 2022-12-13 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conversation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConversationReplyFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=500, upload_to='static/uploads/default/conversation-reply/%Y/%m/%d/')),
                ('conversation_reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conversation.conversationreply')),
            ],
        ),
    ]