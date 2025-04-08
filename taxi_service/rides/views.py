from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view
from .models import Driver, Ride
from .serializers import DriverSerializer, RideSerializer
from django.db.models import F
from geopy.distance import geodesic
from rest_framework.views import APIView
from .serializers import DriverSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .utils import find_nearest_driver
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

class AvailableDriversView(generics.ListAPIView):
    queryset = Driver.objects.filter(is_available=True)
    serializer_class = DriverSerializer

@csrf_exempt
@api_view(['POST'])
def request_ride(request):
    try:
        pickup_latitude = request.data.get('pickup_latitude')
        pickup_longitude = request.data.get('pickup_longitude')
        drop_latitude = request.data.get('drop_latitude')
        drop_longitude = request.data.get('drop_longitude')
        customer_id = request.data.get('customer')

        if not all([pickup_latitude, pickup_longitude, drop_latitude, drop_longitude, customer_id]):
            return Response({"error": "Missing required fields"}, status=400)

        try:
            customer = User.objects.get(id=customer_id)
        except User.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

        fare = calculate_fare(pickup_latitude, pickup_longitude, drop_latitude, drop_longitude)

        ride = Ride.objects.create(
            customer=customer,
            pickup_latitude=pickup_latitude,
            pickup_longitude=pickup_longitude,
            drop_latitude=drop_latitude,
            drop_longitude=drop_longitude,
            fare=fare  
        )

        serializer = RideSerializer(ride)
        return Response(serializer.data, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@csrf_exempt
@api_view(['GET'])
def find_driver_api(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
        
        nearest_driver = find_nearest_driver(ride.pickup_latitude, ride.pickup_longitude)

        if nearest_driver:
            return JsonResponse({"driver_id": nearest_driver.id, "message": "Driver found!"})
        else:
            return JsonResponse({"message": "No drivers available"}, status=404)

    except Ride.DoesNotExist:
        return JsonResponse({"error": "Ride not found"}, status=404)


@csrf_exempt
@api_view(["PATCH"])
def update_driver_location(request, driver_id):
    try:
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        if latitude is None or longitude is None:
            return Response({"error": "Latitude and Longitude required"}, status=status.HTTP_400_BAD_REQUEST)

        updated = Driver.objects.filter(id=driver_id).update(latitude=latitude, longitude=longitude)

        if updated:
            driver = Driver.objects.get(id=driver_id)
            return Response(DriverSerializer(driver).data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
def cancel_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)

        cancellation_fare = calculate_fare(
            ride.pickup_latitude, 
            ride.pickup_longitude, 
            ride.drop_latitude, 
            ride.drop_longitude, 
            cancelled=True  
        )

        ride.status = "Cancelled"
        ride.fare = cancellation_fare  
        ride.save()

        return Response({"message": "Ride cancelled successfully", "updated_fare": cancellation_fare}, status=200)

    except Ride.DoesNotExist:
        return Response({"error": "Ride not found"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


def calculate_fare(pickup_latitude, pickup_longitude, drop_latitude, drop_longitude, cancelled=False):
    pickup_location = (pickup_latitude, pickup_longitude)
    drop_location = (drop_latitude, drop_longitude)
    distance_km = geodesic(pickup_location, drop_location).km  
    base_fare = 50 
    per_km_rate = 10  
    fare = base_fare + (distance_km * per_km_rate)

    if cancelled:
        cancellation_fee = 0.05 * fare  
        fare += cancellation_fee

    return round(fare, 2) 
