from django.db import models
from django.contrib.auth.models import User
from abc import ABC, abstractmethod

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=5.0)
    car_type = models.CharField(max_length=50, default="Sedan")  

class LocationService:
    @staticmethod
    def update_driver_location(driver, lat, lon):
        driver.latitude = lat
        driver.longitude = lon
        driver.save()

class CancellationPolicy:
    @staticmethod
    def calculate_cancellation_fee(fare):
        return round(fare * 0.05, 2)

class RideService:
    def __init__(self, driver_finder):
        self.driver_finder = driver_finder

    def assign_driver(self, ride):
        nearest_driver = self.driver_finder.find_nearest(ride.pickup_latitude, ride.pickup_longitude)
        if nearest_driver:
            ride.driver = nearest_driver
            nearest_driver.is_available = False
            nearest_driver.save()
            ride.save()

REASONS = [
    ('Driver delayed', 'Driver delayed'),
    ('Change of plans', 'Change of plans'),
    ('Found another ride', 'Found another ride'),
]

class Ride(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    drop_latitude = models.FloatField()
    drop_longitude = models.FloatField()
    car_type = models.CharField(max_length=50, default="Sedan")   
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ], default='Pending')
    fare = models.FloatField(default=0.0)  
    cancellation_fee = models.FloatField(default=0.0)
    estimated_time = models.CharField(max_length=50, null=True, blank=True)
    cancellation_reason = models.CharField(max_length=50, choices=REASONS, null=True, blank=True)

    def cancel_ride(self, reason):
        self.status = 'Cancelled'
        self.cancellation_fee = CancellationPolicy.calculate_cancellation_fee(self.fare)
        self.cancellation_reason = reason
        self.save()
