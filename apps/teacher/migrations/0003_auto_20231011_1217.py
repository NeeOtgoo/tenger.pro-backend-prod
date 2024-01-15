# Generated by Django 3.2.20 on 2023-10-11 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_employee_compartment'),
        ('teacher', '0002_auto_20221006_1336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='access',
        ),
        migrations.AlterField(
            model_name='teacher',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='birth_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.city'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='birth_district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.district'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='join_before',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='join_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='phone2',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
