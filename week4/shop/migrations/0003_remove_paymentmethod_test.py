# Generated by Django 5.0.6 on 2024-07-25 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_paymentmethod_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentmethod',
            name='test',
        ),
    ]
