# Generated by Django 3.2.15 on 2022-09-19 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='credit',
            field=models.IntegerField(),
        ),
    ]
