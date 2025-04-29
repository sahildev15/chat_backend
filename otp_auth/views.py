from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EmailOTP
from .serializer import EmailSerializer, OTPVerifySerializer
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

# users/models.py

# users/views.py



class SendOTPView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_obj, created = EmailOTP.objects.get_or_create(email=email)
            otp_obj.generate_otp()
            
            # Send email
            send_mail(
                subject='Your OTP Code',
                message=f'Your OTP is {otp_obj.otp}',
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )
            return Response({"message": "OTP sent to email successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                otp_obj = EmailOTP.objects.get(email=email)
                if otp_obj.otp == otp:
                    otp_obj.is_verified = True
                    otp_obj.save()
                    
                    # Get or create the user
                    User = get_user_model()
                    user, created = User.objects.get_or_create(email=email)

                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    refresh_token = str(refresh)

                    # Check if user has completed profile
                    user_registered = bool(user.first_name and user.last_name and user.phone_number)

                    return Response({
                        "message": "OTP verified successfully.",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user_registered": user_registered
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
            except EmailOTP.DoesNotExist:
                return Response({"error": "Email not found."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
