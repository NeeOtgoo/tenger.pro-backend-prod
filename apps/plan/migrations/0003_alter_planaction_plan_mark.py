# Generated by Django 3.2.18 on 2023-05-17 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0002_alter_plan_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planaction',
            name='plan_mark',
            field=models.TextField(blank=True),
        ),
    ]
