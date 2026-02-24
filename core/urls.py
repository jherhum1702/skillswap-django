from django.urls import path
from .views import *
app_name = 'core'

urlpatterns = [
path('login/', CustomLogin.as_view(), name='login'),
path('registro/', CustomRegisterView.as_view(), name='registro'),
path('', Postview.as_view(), name='home'),
]