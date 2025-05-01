
from rest_framework import serializers
from .models import Driver, Ride

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'latitude', 'longitude', 'is_available', 'car_type', 'rating']

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'customer', 'driver', 'pickup_latitude', 'pickup_longitude', 
                  'drop_latitude', 'drop_longitude', 'status', 'estimated_time']

