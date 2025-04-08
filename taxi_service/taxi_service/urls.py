from django.contrib import admin
from django.urls import path, include
from rides.views import (
    request_ride, update_driver_location, cancel_ride, 
    AvailableDriversView,find_driver_api
)

urlpatterns = [
    path('admin/',admin.site.urls),
    path('drivers/', AvailableDriversView.as_view(), name='available_drivers'),
    path('ride/request/', request_ride, name='request_ride'),
    path('driver/update-location/<int:driver_id>/', update_driver_location, name='update_driver_location'),
    path('ride/cancel/<int:ride_id>/', cancel_ride, name='cancel_ride'),
    path("find-driver/<int:ride_id>/", find_driver_api, name="find_driver"),
]
