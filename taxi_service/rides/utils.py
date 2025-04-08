import math
import requests
from geopy.distance import geodesic
from rides.models import Driver 

class DistanceCalculator:    
    @staticmethod
    def geodesic_distance(lat1, lon1, lat2, lon2):
        return geodesic((lat1, lon1), (lat2, lon2)).km

    @staticmethod
    def approximate_distance(lat1, lon1, lat2, lon2):
        lat_avg = (lat1 + lat2) / 2
        lat_dist = 111.32 * (lat2 - lat1)
        lon_dist = (40075 * math.cos(math.radians(lat_avg)) / 360) * (lon2 - lon1)
        return math.sqrt(lat_dist ** 2 + lon_dist ** 2)

def get_available_drivers():
    return Driver.objects.filter(is_available=True)

def find_nearest_driver(pickup_lat, pickup_lng, distance_calculator=DistanceCalculator()):
    available_drivers = get_available_drivers()
    nearest_driver = None
    min_distance = float('inf')

    for driver in available_drivers:
        distance = distance_calculator.geodesic_distance(pickup_lat, pickup_lng, driver.latitude, driver.longitude)
        if distance < min_distance:
            min_distance = distance
            nearest_driver = driver

    return nearest_driver

def get_travel_time(pickup_lat, pickup_lon, drop_lat, drop_lon):
    pass
