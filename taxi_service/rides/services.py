from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Driver, Ride, DeclinedRide, UserProfile
from .utils import DistanceCalculator, FareCalculator, CancellationPolicy
from decimal import Decimal

User = get_user_model()

class DriverService:
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
    @staticmethod
    def get_available_rides(driver):
        print(f"Checking available rides for driver {driver.id}")
        print(f"Driver location: {driver.latitude}, {driver.longitude}")
        print(f"Driver available: {driver.is_available}")
        
        available_rides = Ride.objects.filter(
            status='Pending'
        ).exclude(
            id__in=DeclinedRide.objects.filter(driver=driver).values_list('ride_id', flat=True)
        )
        
        print(f"Total pending rides: {available_rides.count()}")
        
        nearby_rides = []
        for ride in available_rides:
            distance = DistanceCalculator.calculate_distance(
                driver.latitude, driver.longitude,
                ride.pickup_latitude, ride.pickup_longitude
            )
            print(f"Ride {ride.id} - Distance: {distance}km")
            if distance <= 5:  
                ride.distance_to_driver = round(distance, 2)
                nearby_rides.append(ride)
                print(f"Added ride {ride.id} to nearby rides")
                
        print(f"Total nearby rides: {len(nearby_rides)}")
        return nearby_rides

    @staticmethod
    def get_customer_rides(customer):
        return Ride.objects.filter(customer=customer).order_by('-id')

    @staticmethod
    def get_driver_rides(driver):
        return Ride.objects.filter(driver=driver).order_by('-id')

    @staticmethod
    def accept_ride(ride, driver):
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
        if ride.status != 'Pending':
            raise ValidationError("Cannot decline this ride")
        DeclinedRide.objects.create(driver=driver, ride=ride)

    @staticmethod
    def cancel_ride(ride, reason):
        if ride.status in ['Completed', 'Cancelled']:
            raise ValidationError("Cannot cancel this ride")
        
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
        if ride.customer == user and ride.status in ['Pending', 'Accepted']:
            return True
            
        if hasattr(user, 'driver') and ride.driver == user.driver and ride.status not in ['Completed', 'Cancelled']:
            return True
            
        return False

    @staticmethod
    def create_ride(customer, pickup_lat, pickup_lon, drop_lat, drop_lon, car_type="Sedan"):
       
        distance_km = DistanceCalculator.calculate_distance(pickup_lat, pickup_lon, drop_lat, drop_lon)

        fare = Decimal(str(FareCalculator.calculate_fare(distance_km)))

        try:
            customer_profile = customer.userprofile
            if customer_profile.pending_cancellation_fee > 0:
                fare += customer_profile.pending_cancellation_fee
                customer_profile.pending_cancellation_fee = Decimal('0')
                customer_profile.save()
        except UserProfile.DoesNotExist:
            pass 

        estimated_minutes = None
        speed_kph = 60.0 
        penalty_per_unit = 5.0 
        penalty_unit = "hour" 

        if car_type == "SUV":
            speed_kph = 80.0
            penalty_per_unit = 3.0 
            penalty_unit = "km"
        elif car_type == "Premium":
            speed_kph = 100.0
            penalty_per_unit = 2.0
            penalty_unit = "km"

        if speed_kph > 0:
            base_travel_hours = distance_km / speed_kph
            base_travel_minutes = base_travel_hours * 60.0

            if penalty_unit == "hour":
                penalty_minutes = base_travel_hours * penalty_per_unit
            elif penalty_unit == "km":
                 penalty_minutes = distance_km * penalty_per_unit
            else: 
                 penalty_minutes = 0

            estimated_minutes = base_travel_minutes + penalty_minutes
        else: 
            estimated_minutes = float('inf') 

        estimated_time_str = f"{round(estimated_minutes)} minutes" if estimated_minutes is not None and estimated_minutes != float('inf') else "Calculating..." 

        ride = Ride.objects.create(
            customer=customer,
            pickup_latitude=pickup_lat,
            pickup_longitude=pickup_lon,
            drop_latitude=drop_lat,
            drop_longitude=drop_lon,
            car_type=car_type, 
            fare=fare,
            status='Pending',
            estimated_time=estimated_time_str 
        )

        return ride

    @staticmethod
    def complete_ride(ride):
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