# Generated by Django 4.2.2 on 2023-09-03 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_payment_razorpay_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='razorpay_order_id',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]
