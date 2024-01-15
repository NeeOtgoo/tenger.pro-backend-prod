# Generated by Django 3.2.15 on 2022-09-15 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_student_is_paid'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='user',
        ),
        migrations.RemoveField(
            model_name='invoice_stock',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='invoice_stock',
            name='title',
        ),
        migrations.AddField(
            model_name='invoice',
            name='qpay_invoice_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='qpay_qr_image',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='qpay_qr_text',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='qpay_shortUrl',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
        migrations.AddField(
            model_name='invoice_stock',
            name='link',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='invoice_stock',
            name='logo',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='invoice_stock',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='is_current',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='invoice_stock',
            name='description',
            field=models.CharField(max_length=50, null=True),
        ),
    ]