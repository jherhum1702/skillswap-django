from django.contrib.auth.views import LogoutView
from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *
app_name = 'core'


router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'publicaciones', PublicacionViewSet)
router.register(r'acuerdos', AcuerdoViewSet)
router.register(r'sesiones', SesionViewSet)
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
    path('deals/create/', DealsCreateView.as_view(), name='deals-create'),
    path('deals/', DealsListView.as_view(), name='deals'),
    path('deals/<int:pk>/accept/', DealsUpdateAccepView.as_view(), name='deals-accept'),
    path('deals/<int:pk>/cancel/', DealsUpdateCancelView.as_view(), name='deals-cancel'),
    path('deals/<int:pk>/fin/', DealsUpdateFinView.as_view(), name='deals-fin'),
    path('deals/<int:pk>/',DealsDetailView.as_view(), name='deals-detail'),
    path('deals/<int:pk>/start/', DealsUpdateStartView.as_view(), name='deals-start'),
    path('posts/create/', PostCreateview.as_view(), name='post-create'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/close/', PostCloseView.as_view(), name='post-close'),
    path('deals/<int:pk>/sessions/create/', SesionCreateView.as_view(), name='session-create'),
    path('sessions/<int:pk>/', SesionDetailView.as_view(), name='session-detail'),
    path('sessions/', SesionLisView.as_view(), name='sessions'),
    path('api/', include(router.urls)),
]