# Generated by Django 3.2.15 on 2022-09-07 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_employee',
            field=models.BooleanField(default=False),
        ),
    ]
