"""
URL configuration for skillswap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

original_login = admin.site.login

def secure_admin_login(request, **kwargs):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para acceder al panel de administración.')
        return redirect('core:login')
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder al panel de administración.')
        return redirect('core:login')
    return original_login(request, **kwargs)

admin.site.login = secure_admin_login

def secure_api_view(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a la API.')
            return redirect('core:login')
        if not request.user.is_staff and not request.user.is_superuser:
            messages.error(request, 'No tienes permisos para acceder a la API.')
            return redirect('core:login')
        return view_func(request, *args, **kwargs)
    return wrapped

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls'), name='core'),
    path('api/schema/', secure_api_view(SpectacularAPIView.as_view()), name='schema'),
    path('api/docs/', secure_api_view(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
    path('api/redoc/', secure_api_view(SpectacularRedocView.as_view(url_name='schema')), name='redoc'),
]