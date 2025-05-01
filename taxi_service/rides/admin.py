from django.contrib import admin
from .models import Driver, Ride, DeclinedRide

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_available', 'rating', 'car_type')
    list_filter = ('is_available', 'car_type')
    search_fields = ('user__username',)

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'driver', 'status', 'car_type', 'fare')
    list_filter = ('status', 'car_type')
    search_fields = ('customer__username', 'driver__user__username')

@admin.register(DeclinedRide)
class DeclinedRideAdmin(admin.ModelAdmin):
    list_display = ('driver', 'ride', 'declined_at')
    list_filter = ('declined_at',)
    search_fields = ('driver__user__username', 'ride__id')
