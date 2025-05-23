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
    full_name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    license_number = forms.CharField(max_length=50, required=True)
    car_model = forms.CharField(max_length=100, required=True)
    car_plate_number = forms.CharField(max_length=20, required=True)
    car_type = forms.ChoiceField(choices=[
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Premium', 'Premium'),
    ], required=True)
    latitude = forms.FloatField(required=True)
    longitude = forms.FloatField(required=True)

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits")
        return phone

    def clean_license_number(self):
        license_no = self.cleaned_data.get('license_number')
        if len(license_no) < 5:
            raise forms.ValidationError("License number must be at least 5 characters long")
        return license_no

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
        ('Premium', 'Premium'),
    ]) 