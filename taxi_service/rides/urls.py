from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('ride/<int:ride_id>/', views.ride_status, name='ride_status'),
    path('ride/<int:ride_id>/accept/', views.accept_ride, name='accept_ride'),
    path('ride/<int:ride_id>/decline/', views.decline_ride, name='decline_ride'),
    path('ride/<int:ride_id>/cancel/', views.cancel_ride, name='cancel_ride'),
    path('update-location/<int:driver_id>/', views.update_driver_location, name='update_driver_location'),
    path('logout/', views.logout_user, name='logout'),
    path('ride/complete/<int:ride_id>/', views.complete_ride, name='complete_ride'),
    path('driver-location/<int:driver_id>/', views.get_driver_location, name='get_driver_location'),
]
