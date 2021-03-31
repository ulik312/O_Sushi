from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.users.views import *


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('successful-registration/', SuccessfulRegistrationView.as_view(), name='successful-registration'),
    path('activation/', ActivationView.as_view(), name='activation-view'),
    path('login/', SigninView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my-profile/<str:email>/', ProfileView.as_view(), name='user-profile'),
]
