# Generated by Django 3.0.3 on 2020-11-04 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantReservation', '0004_customerphotos_location_reservation_restaurant_restaurantphotos_restauranttables_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='city',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]