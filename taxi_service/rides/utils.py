import math
from geopy.distance import geodesic
from rides.models import Driver 
from decimal import Decimal

class DistanceCalculator:    
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        return geodesic((lat1, lon1), (lat2, lon2)).km

    @staticmethod
    def approximate_distance(lat1, lon1, lat2, lon2):
        lat_avg = (lat1 + lat2) / 2
        lat_dist = 111.32 * (lat2 - lat1)
        lon_dist = (40075 * math.cos(math.radians(lat_avg)) / 360) * (lon2 - lon1)
        return math.sqrt(lat_dist ** 2 + lon_dist ** 2)

def get_available_drivers():
    return Driver.objects.filter(is_available=True)

def find_nearest_driver(pickup_latitude, pickup_longitude, max_distance_km=5):
    available_drivers = Driver.objects.filter(
        is_available=True,
        latitude__isnull=False,
        longitude__isnull=False
    )
    
    nearest_driver = None
    min_distance = float('inf')
    
    for driver in available_drivers:
        distance = DistanceCalculator.calculate_distance(
            pickup_latitude, pickup_longitude,
            driver.latitude, driver.longitude
        )
        
        if distance <= max_distance_km and distance < min_distance:
            min_distance = distance
            nearest_driver = driver
            
    return nearest_driver

class FareCalculator:
    BASE_FARE = Decimal('50.00')  
    PER_KM_RATE = Decimal('10.00')  
    
    @staticmethod
    def calculate_fare(distance_km):
        return FareCalculator.BASE_FARE + (Decimal(str(distance_km)) * FareCalculator.PER_KM_RATE)

class CancellationPolicy:
    CANCELLATION_FEE_PERCENTAGE = Decimal('0.05')  

    @staticmethod
    def calculate_cancellation_fee(fare):
        return fare * CancellationPolicy.CANCELLATION_FEE_PERCENTAGE
