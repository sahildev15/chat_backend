from django.urls import path

from .views import UserRegistrationView, UserUpdateAPi



urlpatterns = [
    path('register/', UserRegistrationView.as_view()),  
    path('profile/', UserRegistrationView.as_view()),
    path('update/', UserUpdateAPi.as_view()),

]
