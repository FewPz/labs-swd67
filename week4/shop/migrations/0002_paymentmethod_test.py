# Generated by Django 5.0.6 on 2024-07-25 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='test',
            field=models.BooleanField(default=False),
        ),
    ]
