# Generated by Django 3.2.15 on 2022-10-06 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0002_alter_subject_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='part',
            field=models.CharField(choices=[('A', 'Ерөнхий суурь хэсэг'), ('B', 'Техникийн /Мэргэжлийн/ суурь хэсэг'), ('C', 'Мэргэшүүлэх хэсэг')], default='A', max_length=50),
        ),
    ]