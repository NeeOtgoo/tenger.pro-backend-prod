# Generated by Django 3.2.15 on 2022-10-06 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employee_attandance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='address_live',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='citizen',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='join_before',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='join_date',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='religion',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='surname',
        ),
    ]
