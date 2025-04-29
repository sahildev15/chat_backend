from rest_framework import serializers

from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','email', 'profile_photo', 'phone_number']
        read_only_fields = ['email']
