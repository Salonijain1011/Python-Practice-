from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class UserProfile(models.Model):
    USER_TYPES = [
        ('driver', 'Driver'),
        ('customer', 'Customer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    pending_cancellation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=5.0)
    car_type = models.CharField(max_length=50, default="Sedan")
    license_number = models.CharField(max_length=50, null=True, blank=True)
    car_model = models.CharField(max_length=100, null=True, blank=True)
    car_plate_number = models.CharField(max_length=20, null=True, blank=True)
    registration_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Driver"

REASONS = [
    ('Pickup location far away', 'Pickup location far away'),
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
    fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    cancellation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_time = models.CharField(max_length=50, null=True, blank=True)
    cancellation_reason = models.CharField(max_length=50, choices=REASONS, null=True, blank=True)

    def cancel_ride(self, reason):
        self.status = 'Cancelled'
        self.cancellation_fee = self.fare * Decimal('0.05')  
        self.cancellation_reason = reason
        self.save()

class DeclinedRide(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    declined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('driver', 'ride')