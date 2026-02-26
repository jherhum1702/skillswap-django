from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *
app_name = 'core'

urlpatterns = [
path('accounts/login/', CustomLogin.as_view(), name='login'),
path('accounts/logout/', LogoutView.as_view(), name='logout'),
path('accounts/register/', CustomRegisterView.as_view(), name='registro'),
path('', Postview.as_view(), name='home'),
path('profile/', ProfileView.as_view(), name='profile'),
path('profile/edit/', ProfileUpdateView.as_view(), name='profile-update'),
]