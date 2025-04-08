import math
import requests
from geopy.distance import geodesic

def calculate_approx_distance(lat1, lon1, lat2, lon2):
    lat_avg = (lat1 + lat2) / 2
    lat_dist = 111.32 * (lat2 - lat1)
    lon_dist = (40075 * math.cos(math.radians(lat_avg)) / 360) * (lon2 - lon1)
    return math.sqrt(lat_dist ** 2 + lon_dist ** 2)

def find_nearest_driver(pickup_lat, pickup_lng):
    from rides.models import Driver 

    available_drivers = Driver.objects.filter(is_available=True)
    nearest_driver = None
    min_distance = float('inf')

    for driver in available_drivers:
        distance = geodesic((pickup_lat, pickup_lng), (driver.latitude, driver.longitude)).km
        if distance < min_distance:
            min_distance = distance
            nearest_driver = driver

    return nearest_driver

def get_travel_time(pickup_lat, pickup_lon, drop_lat, drop_lon):
    pass  
