from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('accounts/login/', CustomLogin.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/register/', CustomRegisterView.as_view(), name='registro'),
    path('posts/', Postlistview.as_view(), name='post'),
    path('posts/<int:pk>', PostDetailview.as_view(), name='detail'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-update'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('change-preference/', change_preference, name='change_preference'),
    path('clear-filters/', clear_filters, name='clear_filters'),
]