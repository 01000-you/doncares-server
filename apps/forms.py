# forms.py

from django import forms
from .models import Driver
from .models import Customer
from django.db.models import Q
from .models import KakaoUser

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'region', 'phone_number', 'app_user_id']
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['app_user_id', 'name', 'region', 'target', 'period']

class KakaoUserForm(forms.ModelForm):
    class Meta:
        model = KakaoUser
        fields = ['nickname', 'profile_image_url', 'phone_number', 'email', 'app_user_id']

    def clean_app_user_id(self):
        app_user_id = self.cleaned_data['app_user_id']
        if KakaoUser.objects.filter(app_user_id=app_user_id).exists():
            # If the app_user_id already exists, update the existing data instead of creating a new one.
            instance = KakaoUser.objects.get(app_user_id=app_user_id)
            self.instance = instance
        return app_user_id