# Generated by Django 3.2.15 on 2023-01-12 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0004_alter_subject_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='mark_variety',
            field=models.IntegerField(choices=[(1, 'Мэдлэгийн үнэлгээ'), (2, 'Чадамжийн үнэлгээ'), (3, 'Түвшингийн үнэлгээ')], default=1),
        ),
    ]
