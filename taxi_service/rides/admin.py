from django.contrib import admin
from .models import Driver, Ride

class DriverFilterMixin:
    list_filter = ('is_available', 'car_type')

class DriverSearchMixin:
    search_fields = ('user__username', 'car_type')

class RideFilterMixin:
    list_filter = ('status', 'car_type')

class RideSearchMixin:
    search_fields = ('customer__username', 'driver__user__username')

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin, DriverFilterMixin, DriverSearchMixin):
    list_display = ('user', 'latitude', 'longitude', 'is_available', 'rating', 'car_type')

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin, RideFilterMixin, RideSearchMixin):
    list_display = ('customer', 'driver', 'pickup_latitude', 'pickup_longitude', 'drop_latitude', 'drop_longitude', 'status', 'fare')
    readonly_fields = ('cancellation_fee', 'cancellation_reason')
