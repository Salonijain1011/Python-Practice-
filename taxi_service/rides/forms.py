from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ride, UserProfile

class UserRegistrationForm(UserCreationForm):
    USER_TYPES = [
        ('driver', 'Driver'),
        ('customer', 'Customer'),
    ]
    
    user_type = forms.ChoiceField(choices=USER_TYPES)
    phone_number = forms.CharField(max_length=15)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'phone_number')

class DriverRegistrationForm(forms.Form):
    license_number = forms.CharField(max_length=50)
    car_model = forms.CharField(max_length=100)
    car_plate_number = forms.CharField(max_length=20)
    car_type = forms.ChoiceField(choices=[
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Luxury', 'Luxury'),
    ])

class RideBookingForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['pickup_latitude', 'pickup_longitude', 'drop_latitude', 'drop_longitude', 'car_type']
        widgets = {
            'pickup_latitude': forms.HiddenInput(),
            'pickup_longitude': forms.HiddenInput(),
            'drop_latitude': forms.HiddenInput(),
            'drop_longitude': forms.HiddenInput(),
        }
    
    pickup_address = forms.CharField(max_length=255)
    drop_address = forms.CharField(max_length=255)
    car_type = forms.ChoiceField(choices=[
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Luxury', 'Luxury'),
    ]) 