from django.contrib import admin
from django.urls import path, include
from rides.views import (
    request_ride, update_driver_location, cancel_ride, 
    AvailableDriversView, find_driver_api, book_ride, ride_details,
    login_view, register_view, logout_user, driver_dashboard, accept_ride, decline_ride
)

urlpatterns = [
    path('', login_view, name='login'), 
    path('admin/', admin.site.urls),
    path('book/', book_ride, name='book_ride'),
    path('drivers/', AvailableDriversView.as_view(), name='available_drivers'),
    path('ride/request/', request_ride, name='request_ride'),
    path('driver/update-location/<int:driver_id>/', update_driver_location, name='update_driver_location'),
    path('ride/cancel/<int:ride_id>/', cancel_ride, name='cancel_ride'),
    path("find-driver/<int:ride_id>/", find_driver_api, name="find_driver"),
    path("ride/<int:ride_id>/", ride_details, name="ride_details"),
    path('driver/dashboard/', driver_dashboard, name='driver_dashboard'),
    path('ride/accept/<int:ride_id>/', accept_ride, name='accept_ride'),
    path('ride/decline/<int:ride_id>/', decline_ride, name='decline_ride'),
    path('', include('rides.urls')), 
]
