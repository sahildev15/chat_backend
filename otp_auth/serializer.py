from rest_framework import serializers
from .models import EmailOTP

# users/serializers.py
from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

