# Generated by Django 4.2.2 on 2023-09-03 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_payment_orderplaced'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
