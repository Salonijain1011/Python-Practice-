from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view
from .models import Driver, Ride
from .serializers import DriverSerializer, RideSerializer
from geopy.distance import geodesic
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import find_nearest_driver

class AvailableDriversView(generics.ListAPIView):
    queryset = Driver.objects.filter(is_available=True)
    serializer_class = DriverSerializer

def validate_request_data(request, required_fields):
    if not all(request.data.get(field) for field in required_fields):
        return Response({"error": "Missing required fields"}, status=400)
    return None

def get_customer_by_id(customer_id):
    try:
        return User.objects.get(id=customer_id)
    except User.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)

@csrf_exempt
@api_view(['POST'])
def request_ride(request):
    validation_response = validate_request_data(request, ['pickup_latitude', 'pickup_longitude', 'drop_latitude', 'drop_longitude', 'customer'])
    if validation_response:
        return validation_response

    customer = get_customer_by_id(request.data.get('customer'))
    if isinstance(customer, Response):  
        return customer

    fare = calculate_fare(request.data.get('pickup_latitude'), request.data.get('pickup_longitude'), request.data.get('drop_latitude'), request.data.get('drop_longitude'))

    ride = Ride.objects.create(
        customer=customer,
        pickup_latitude=request.data.get('pickup_latitude'),
        pickup_longitude=request.data.get('pickup_longitude'),
        drop_latitude=request.data.get('drop_latitude'),
        drop_longitude=request.data.get('drop_longitude'),
        fare=fare  
    )

    return Response(RideSerializer(ride).data, status=201)

@csrf_exempt
@api_view(['GET'])
def find_driver_api(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
        nearest_driver = find_nearest_driver(ride.pickup_latitude, ride.pickup_longitude)

        if nearest_driver:
            return JsonResponse({"driver_id": nearest_driver.id, "message": "Driver found!"})
        return JsonResponse({"message": "No drivers available"}, status=404)

    except Ride.DoesNotExist:
        return JsonResponse({"error": "Ride not found"}, status=404)

@csrf_exempt
@api_view(["PATCH"])
def update_driver_location(request, driver_id):
    latitude = request.data.get("latitude")
    longitude = request.data.get("longitude")

    if latitude is None or longitude is None:
        return Response({"error": "Latitude and Longitude required"}, status=status.HTTP_400_BAD_REQUEST)

    updated = Driver.objects.filter(id=driver_id).update(latitude=latitude, longitude=longitude)

    if updated:
        return Response(DriverSerializer(Driver.objects.get(id=driver_id)).data, status=status.HTTP_200_OK)
    return Response({"error": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
def cancel_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
        ride.fare = calculate_fare(ride.pickup_latitude, ride.pickup_longitude, ride.drop_latitude, ride.drop_longitude, cancelled=True)
        ride.status = "Cancelled"
        ride.save()

        return Response({"message": "Ride cancelled successfully", "updated_fare": ride.fare}, status=200)

    except Ride.DoesNotExist:
        return Response({"error": "Ride not found"}, status=404)

def calculate_fare(pickup_latitude, pickup_longitude, drop_latitude, drop_longitude, cancelled=False):
    distance_km = geodesic((pickup_latitude, pickup_longitude), (drop_latitude, drop_longitude)).km  
    fare = 50 + (distance_km * 10)  

    if cancelled:
        fare += 0.05 * fare  

    return round(fare, 2)
