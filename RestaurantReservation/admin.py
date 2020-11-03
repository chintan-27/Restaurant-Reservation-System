from django.contrib import admin
from RestaurantReservation.models import User, Location, Restaurant, RestaurantTables, Reservation, Review, RestaurantPhotos, CustomerPhotos
# Register your models here.

admin.site.register(User)
admin.site.register(Location)
admin.site.register(Restaurant)
admin.site.register(RestaurantTables)
admin.site.register(Reservation)
admin.site.register(Review)
admin.site.register(RestaurantPhotos)
admin.site.register(CustomerPhotos)
