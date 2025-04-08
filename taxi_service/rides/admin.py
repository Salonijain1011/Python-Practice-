from django.contrib import admin
from .models import Driver, Ride

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'latitude', 'longitude', 'is_available', 'rating', 'car_type')
    list_filter = ('is_available', 'car_type')
    search_fields = ('user__username', 'car_type')

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('customer', 'driver', 'pickup_latitude', 'pickup_longitude', 'drop_latitude', 'drop_longitude', 'status', 'fare')
    list_filter = ('status', 'car_type')
    search_fields = ('customer__username', 'driver__user__username')
    readonly_fields = ('cancellation_fee', 'cancellation_reason')

