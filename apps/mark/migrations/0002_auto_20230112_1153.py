# Generated by Django 3.2.15 on 2023-01-12 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mark', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark_board',
            name='mark_variety',
            field=models.IntegerField(choices=[(1, 'Мэдлэгийн үнэлгээ'), (2, 'Чадамжийн үнэлгээ'), (3, 'Түвшингийн үнэлгээ')], default=1),
        ),
        migrations.AddField(
            model_name='mark_setting',
            name='mark_variety',
            field=models.IntegerField(choices=[(1, 'Мэдлэгийн үнэлгээ'), (2, 'Чадамжийн үнэлгээ'), (3, 'Түвшингийн үнэлгээ')], default=1),
        ),
    ]
