from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .forms import *


# Create your views here.

class Postview(ListView):
    model = Publicacion
    template_name = 'core/publicacion_list.html'
    context_object_name = 'posts'




class CustomLogin(LoginView):
    form_class = CustomloginForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('core:home')



class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        user = form.save()
        user_group, created = Group.objects.get_or_create(name='Usuario')
        user.groups.add(user_group)
        login(self.request, user)
        return super().form_valid(form)
