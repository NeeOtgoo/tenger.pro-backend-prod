# Generated by Django 3.2.15 on 2022-10-12 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('online_lesson', '0003_online_student_create_userid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='online_student',
            name='create_userID',
        ),
        migrations.AddField(
            model_name='online_file_folder',
            name='create_userID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
