# Generated by Django 3.0.6 on 2020-10-30 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantReservation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='usertype',
            field=models.CharField(choices=[('restaurant', 'RESTAURANT'), ('customer', 'CUSTOMER')], default='customer', max_length=15),
        ),
    ]
