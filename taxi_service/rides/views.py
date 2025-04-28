from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from geopy.distance import geodesic
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.conf import settings
from datetime import datetime, timedelta

from .models import Driver, Ride, DeclinedRide, UserProfile
from .serializers import DriverSerializer, RideSerializer
from .utils import find_nearest_driver, DistanceCalculator
from .forms import UserRegistrationForm, DriverRegistrationForm, RideBookingForm
from .services import DriverService, RideService

import json
import requests

User = get_user_model()


@csrf_exempt
def register_view(request):
    """Register a new user as driver or customer."""
    if request.method == "GET":
        return render(request, "register.html")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        role = request.POST.get("role", "").strip()

        if not username or not password or not role:
            return JsonResponse({"success": False, "error": "Missing fields"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "error": "Username already taken"}, status=400)

        user = User.objects.create_user(username=username, password=password)

        if role == "driver":
            Driver.objects.create(user=user, is_available=True)
            request.session["role"] = "driver"
        elif role == "customer":
            request.session["role"] = "customer"

        login(request, user)
        return JsonResponse({"success": True, "message": "User registered successfully!", "redirect_url": "/login/"})

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


@csrf_exempt
def login_view(request):
    """Authenticate user login."""
    if request.method == "GET":
        return render(request, "login.html")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            try:
                if hasattr(user, 'driver'):
                    return JsonResponse({"success": True, "message": "Login successful!", "redirect_url": "/driver/dashboard/"})
            except:
                pass
            return JsonResponse({"success": True, "message": "Login successful!", "redirect_url": "/book/"})
        return JsonResponse({"success": False, "error": "Invalid credentials"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


@csrf_exempt
def logout_user(request):
    """Log out the current user."""
    logout(request)
    return redirect("login")


class AvailableDriversView(generics.ListAPIView):
    """List all available drivers."""
    queryset = Driver.objects.filter(is_available=True)
    serializer_class = DriverSerializer


def validate_request_data(request, required_fields):
    """Ensure required fields are in request."""
    if not all(request.data.get(field) for field in required_fields):
        return Response({"error": "Missing required fields"}, status=400)
    return None


def get_customer_by_id(customer_id):
    """Fetch customer by user ID."""
    try:
        return User.objects.get(id=customer_id)
    except User.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)


@csrf_exempt
@api_view(['POST'])
def request_ride(request):
    """Create a new ride request."""
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
    """Assign the nearest driver to the ride."""
    try:
        ride = Ride.objects.get(id=ride_id)

        if ride.status != "Pending":
            return JsonResponse({"error": "This ride has already been assigned or completed."}, status=400)

        nearest_driver = find_nearest_driver(ride.pickup_latitude, ride.pickup_longitude)

        if nearest_driver:
            nearest_driver.is_available = False
            nearest_driver.save()

            ride.driver = nearest_driver
            ride.status = "Accepted"
            ride.save()

            return JsonResponse({
                "driver_id": nearest_driver.id,
                "driver_name": nearest_driver.user.username,
                "latitude": nearest_driver.latitude,
                "longitude": nearest_driver.longitude,
                "status": "Accepted",
                "message": "Nearest driver assigned successfully!"
            })

        return JsonResponse({"message": "No available drivers nearby"}, status=404)

    except Ride.DoesNotExist:
        return JsonResponse({"error": "Ride not found"}, status=404)

@login_required
def accept_ride(request, ride_id):
    if request.method != 'POST':
        return redirect('driver_dashboard')
        
    try:
        ride = Ride.objects.get(id=ride_id)
        driver = DriverService.get_driver_by_user(request.user)
        RideService.accept_ride(ride, driver)
        messages.success(request, "Ride accepted successfully!")
    except (Ride.DoesNotExist, ValidationError) as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, "An error occurred while accepting the ride.")
    return redirect('driver_dashboard')

@login_required
def decline_ride(request, ride_id):
    if request.method != 'POST':
        return redirect('driver_dashboard')
        
    try:
        ride = Ride.objects.get(id=ride_id)
        driver = DriverService.get_driver_by_user(request.user)
        RideService.decline_ride(ride, driver)
        messages.success(request, "Ride declined successfully.")
    except (Ride.DoesNotExist, ValidationError) as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, "An error occurred while declining the ride.")
    return redirect('driver_dashboard')

@csrf_exempt
@login_required
def update_driver_location(request, driver_id):
    try:
        driver = Driver.objects.get(id=driver_id, user=request.user)
        if request.method == 'POST':
            data = json.loads(request.body)
            DriverService.update_location(driver, data['latitude'], data['longitude'])
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    except Driver.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Driver not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except KeyError:
        return JsonResponse({'status': 'error', 'message': 'Missing latitude or longitude'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def cancel_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
        
        if not RideService.can_cancel_ride(ride, request.user):
            messages.error(request, "You cannot cancel this ride.")
            return redirect('dashboard')
            
        if request.method == 'POST':
            reason = request.POST.get('reason', 'No reason provided')
            RideService.cancel_ride(ride, reason)
            messages.success(request, "Ride cancelled successfully.")
            return redirect('dashboard')
        
        return render(request, 'rides/cancel_ride.html', {
            'ride': ride,
            'reasons': [
                ('Too far', 'Pickup location is too far'),
                ('No driver', 'No driver available'),
                ('Change of plans', 'Change of plans'),
                ('Other', 'Other reason')
            ]
        })
    except Ride.DoesNotExist:
        messages.error(request, "Ride not found.")
        return redirect('dashboard')
    except ValidationError as e:
        messages.error(request, str(e))
        return redirect('dashboard')
    except Exception as e:
        messages.error(request, "An error occurred while cancelling the ride.")
        return redirect('dashboard')


def calculate_fare(pickup_latitude, pickup_longitude, drop_latitude, drop_longitude, cancelled=False):
    """Calculate fare based on geodesic distance."""
    distance_km = geodesic((pickup_latitude, pickup_longitude), (drop_latitude, drop_longitude)).km
    fare = 50 + (distance_km * 10)
    if cancelled:
        fare += 0.05 * fare
    return round(fare, 2)


@login_required
def book_ride(request):
    """Book a ride as a customer."""
    
    if request.method == "POST":
        try:
            print(request)
            pickup_latitude = float(request.POST.get("pickup_latitude"))
            pickup_longitude = float(request.POST.get("pickup_longitude"))
            drop_latitude = float(request.POST.get("drop_latitude"))
            drop_longitude = float(request.POST.get("drop_longitude"))
            print(pickup_latitude, pickup_longitude, drop_latitude, drop_longitude)
        except (ValueError, TypeError):
            return render(request, "book_ride.html", {"error": "Invalid or missing coordinates."})

        try:
            ride = RideService.create_ride(
                request.user,
                pickup_latitude,
                pickup_longitude,
                drop_latitude,
                drop_longitude
            )
            # ride_id=10
            # return redirect("ride_details", ride_id=ride.id)
            return redirect('dashboard')
        except ValidationError as e:
            return render(request, "book_ride.html", {"error": str(e)})
        except Exception as e:
            return render(request, "book_ride.html",  {"error": str(e)})

    return render(request, "book_ride.html")


@login_required
def ride_details(request, ride_id):
    """View details of a specific ride."""
    try:
        ride = get_object_or_404(Ride, id=ride_id)
        return render(request, "rides/ride_details.html", {
            "ride": ride,
            "MAPBOX_ACCESS_TOKEN": settings.MAPBOX_ACCESS_TOKEN
        })
    except Exception as e:
        messages.error(request, "Error loading ride details.")
        return redirect('dashboard')


@login_required
def customer_dashboard(request):
    try:
        customer_rides = RideService.get_customer_rides(request.user)
        return render(request, 'rides/customer_dashboard.html', {
            'customer_rides': customer_rides
        })
    except Exception as e:
        messages.error(request, "Error loading dashboard. Please try again.")
        return redirect('login')

@login_required
def driver_dashboard(request):
    try:
        driver = DriverService.get_driver_by_user(request.user)
        available_rides = RideService.get_available_rides(driver)
        driver_rides = RideService.get_driver_rides(driver)
        
        for ride in available_rides:
            ride.distance_to_driver = DistanceCalculator.calculate_distance(
                driver.latitude, driver.longitude,
                ride.pickup_latitude, ride.pickup_longitude
            )
            
        return render(request, 'rides/driver_dashboard.html', {
            'driver': driver,
            'available_rides': available_rides,
            'driver_rides': driver_rides,
            'MAPBOX_ACCESS_TOKEN': settings.MAPBOX_ACCESS_TOKEN
        })
    except Exception as e:
        messages.error(request, str(e))
        return redirect('login')

@login_required
def dashboard(request):
    """Main dashboard that redirects to appropriate dashboard based on user type"""
    try:
        if hasattr(request.user, 'driver'):
            return driver_dashboard(request)
        else:
            return customer_dashboard(request)
    except Exception as e:
        messages.error(request, "Error loading dashboard. Please try again.")
        return redirect('login')

@login_required
def ride_status(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
        return render(request, 'rides/ride_status.html', {
            'ride': ride,
            'MAPBOX_ACCESS_TOKEN': settings.MAPBOX_ACCESS_TOKEN
        })
    except Ride.DoesNotExist:
        messages.error(request, "Ride not found.")
        return redirect('dashboard')

@login_required
def complete_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
        driver = DriverService.get_driver_by_user(request.user)
        
        if ride.driver != driver:
            messages.error(request, "You are not assigned to this ride.")
            return redirect('driver_dashboard')
            
        RideService.complete_ride(ride)
        messages.success(request, "Ride completed successfully!")
    except (Ride.DoesNotExist, ValidationError) as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, "An error occurred while completing the ride.")
    
    return redirect('driver_dashboard')

@login_required
def get_driver_location(request, driver_id):
    try:
        driver = Driver.objects.get(id=driver_id)
        return JsonResponse({
            'success': True,
            'latitude': driver.latitude,
            'longitude': driver.longitude
        })
    except Driver.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Driver not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
