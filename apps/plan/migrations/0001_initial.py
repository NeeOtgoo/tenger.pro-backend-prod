# Generated by Django 3.2.15 on 2022-11-29 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0005_rename_employee_compartment_employee_compartment'),
        ('subject', '0004_alter_subject_credit'),
        ('section', '0001_initial'),
        ('schoolyear', '0001_initial'),
        ('teacher', '0002_auto_20221006_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('topic', models.CharField(max_length=50)),
                ('subject_topic', models.CharField(max_length=50)),
                ('intention', models.TextField(blank=True)),
                ('keyword', models.CharField(max_length=100)),
                ('consumables', models.TextField(blank=True)),
                ('duration', models.IntegerField()),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
                ('schoolyear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolyear.schoolyear')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='section.section')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subject.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='PlanMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PlanAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('teaching_method', models.CharField(max_length=100)),
                ('teacher_activity', models.TextField(blank=True)),
                ('student_activity', models.TextField(blank=True)),
                ('student_assignment', models.TextField(blank=True)),
                ('duration', models.IntegerField()),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.plan')),
                ('plan_mark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.planmark')),
            ],
        ),
    ]
