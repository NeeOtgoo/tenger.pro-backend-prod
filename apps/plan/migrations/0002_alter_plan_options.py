# Generated by Django 3.2.15 on 2022-12-05 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plan',
            options={'permissions': [('approve_plan', 'Can approve plan')]},
        ),
    ]
