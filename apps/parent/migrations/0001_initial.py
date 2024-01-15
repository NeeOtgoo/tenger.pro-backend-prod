# Generated by Django 3.2.6 on 2022-05-02 12:49

import apps.parent.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_name', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('photo', models.ImageField(default='default.jpg', upload_to=apps.parent.models.user_directory_path)),
                ('profession', models.CharField(max_length=50)),
                ('phone', models.CharField(blank=True, max_length=8)),
                ('phone2', models.CharField(blank=True, max_length=8)),
                ('address', models.TextField(blank=True)),
                ('address_live', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('create_userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_create_userID', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]