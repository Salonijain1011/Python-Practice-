from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Driver, Ride, DeclinedRide, UserProfile
from .utils import DistanceCalculator, FareCalculator, CancellationPolicy
from decimal import Decimal

User = get_user_model()

class DriverService:
    """Handle driver-related operations"""
    @staticmethod
    def get_driver_by_user(user):
        try:
            return Driver.objects.get(user=user)
        except Driver.DoesNotExist:
            raise ValidationError("User is not a driver")

    @staticmethod
    def update_location(driver, latitude, longitude):
        driver.latitude = latitude
        driver.longitude = longitude
        driver.save()

    @staticmethod
    def is_driver_available(driver):
        return not Ride.objects.filter(
            driver=driver,
            status__in=['Accepted', 'In Progress']
        ).exists()

    @staticmethod
    def find_nearest_driver(pickup_lat, pickup_lon, max_distance_km=5):
        """Find nearest available driver within specified radius"""
        available_drivers = Driver.objects.filter(
            is_available=True,
            latitude__isnull=False,
            longitude__isnull=False
        )
        
        nearest_driver = None
        min_distance = float('inf')
        
        for driver in available_drivers:
            distance = DistanceCalculator.calculate_distance(
                pickup_lat, pickup_lon,
                driver.latitude, driver.longitude
            )
            if distance <= max_distance_km and distance < min_distance:
                min_distance = distance
                nearest_driver = driver
                
        return nearest_driver

class RideService:
    """Handle ride-related operations"""
    @staticmethod
    def get_available_rides(driver):
        """Get available rides within 5km radius of driver"""
        available_rides = Ride.objects.filter(
            status='Pending'
        ).exclude(
            id__in=DeclinedRide.objects.filter(driver=driver).values_list('ride_id', flat=True)
        )
        
        nearby_rides = []
        for ride in available_rides:
            distance = DistanceCalculator.calculate_distance(
                driver.latitude, driver.longitude,
                ride.pickup_latitude, ride.pickup_longitude
            )
            if distance <= 5:  
                ride.distance_to_driver = round(distance, 2)
                nearby_rides.append(ride)
                
        return nearby_rides

    @staticmethod
    def get_customer_rides(customer):
        """Get all rides for a customer"""
        return Ride.objects.filter(customer=customer).order_by('-id')

    @staticmethod
    def get_driver_rides(driver):
        """Get all rides for a driver"""
        return Ride.objects.filter(driver=driver).order_by('-id')

    @staticmethod
    def accept_ride(ride, driver):
        """Accept a ride request"""
        if not DriverService.is_driver_available(driver):
            raise ValidationError("Driver is already on a ride")
        
        if ride.status != 'Pending' or ride.driver:
            raise ValidationError("Ride is no longer available")
        
        ride.driver = driver
        ride.status = 'Accepted'
        driver.is_available = False
        driver.save()
        ride.save()

    @staticmethod
    def decline_ride(ride, driver):
        """Decline a ride request"""
        if ride.status != 'Pending':
            raise ValidationError("Cannot decline this ride")
        DeclinedRide.objects.create(driver=driver, ride=ride)

    @staticmethod
    def cancel_ride(ride, reason):
        """Cancel a ride and handle cancellation fees"""
        if ride.status in ['Completed', 'Cancelled']:
            raise ValidationError("Cannot cancel this ride")
        
        # Calculate cancellation fee using Decimal
        cancellation_fee = ride.fare * Decimal('0.05')
        
        ride.status = 'Cancelled'
        ride.cancellation_reason = reason
        ride.cancellation_fee = cancellation_fee
        
        if ride.customer:
            try:
                customer_profile = ride.customer.userprofile
                customer_profile.pending_cancellation_fee = cancellation_fee
                customer_profile.save()
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(
                    user=ride.customer,
                    pending_cancellation_fee=cancellation_fee
                )
        
        if ride.driver:
            ride.driver.is_available = True
            ride.driver.save()
            
        ride.save()

    @staticmethod
    def can_cancel_ride(ride, user):
        """Check if user can cancel the ride"""
        if ride.customer == user and ride.status in ['Pending', 'Accepted']:
            return True
            
        if hasattr(user, 'driver') and ride.driver == user.driver and ride.status not in ['Completed', 'Cancelled']:
            return True
            
        return False

    @staticmethod
    def create_ride(customer, pickup_lat, pickup_lon, drop_lat, drop_lon):
        """Create a new ride request"""
        distance = DistanceCalculator.calculate_distance(pickup_lat, pickup_lon, drop_lat, drop_lon)
        fare = Decimal(str(FareCalculator.calculate_fare(distance)))
        
        try:
            customer_profile = customer.userprofile
            if customer_profile.pending_cancellation_fee > 0:
                fare += customer_profile.pending_cancellation_fee
                customer_profile.pending_cancellation_fee = Decimal('0')
                customer_profile.save()
        except UserProfile.DoesNotExist:
            pass
            
        ride = Ride.objects.create(
            customer=customer,
            pickup_latitude=pickup_lat,
            pickup_longitude=pickup_lon,
            drop_latitude=drop_lat,
            drop_longitude=drop_lon,
            fare=fare,
            status='Pending'
        )
        
        return ride

    @staticmethod
    def complete_ride(ride):
        """Complete a ride"""
        if ride.status != 'Accepted':
            raise ValidationError("Cannot complete this ride")
        
        ride.status = 'Completed'
        ride.save()
        
        if ride.driver:
            DriverService.update_location(
                ride.driver,
                ride.drop_latitude,
                ride.drop_longitude
            )
            ride.driver.is_available = True
            ride.driver.save() 