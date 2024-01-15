# Generated by Django 3.2.6 on 2022-05-02 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subject', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Online_test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('create_userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='online_test_create_userID', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subject.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=500)),
                ('hint', models.TextField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/uploads/default/online_test/%Y/%m/%d/')),
                ('answer_type', models.CharField(choices=[('CHOOSE', 'Нэг сонголт'), ('MULTIPLE', 'Олон сонголт'), ('TEXT', 'Бичвэр')], max_length=10)),
                ('online_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_test.online_test')),
            ],
        ),
        migrations.CreateModel(
            name='Question_level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Take_test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('start_at', models.DateTimeField()),
                ('end_at', models.DateTimeField()),
                ('duration', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('OPEN', 'Нээлттэй'), ('CLOSED', 'Хаалттай')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('create_userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='take_test_create_userID', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Take_level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('take_number', models.IntegerField(default=0)),
                ('online_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_test.online_test')),
                ('question_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_test.question_level')),
                ('take_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_test.take_test')),
            ],
        ),
        migrations.CreateModel(
            name='Question_choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(max_length=500)),
                ('score', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_test.question')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='question_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_test.question_level'),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started', models.DateTimeField(blank=True, null=True)),
                ('completed', models.DateTimeField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
                ('take_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_test.take_test')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(max_length=500)),
                ('choices', models.TextField(default='', max_length=2500)),
                ('answer_type', models.CharField(choices=[('CHOOSE', 'Нэг сонголт'), ('MULTIPLE', 'Олон сонголт'), ('TEXT', 'Бичвэр')], default='CHOOSE', max_length=10)),
                ('given_answer', models.TextField(default='', max_length=500)),
                ('score', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_test.participant')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_test.question')),
            ],
        ),
    ]
