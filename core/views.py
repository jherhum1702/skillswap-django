from Tools.i18n.msgfmt import usage

from django.contrib.auth import user_logged_in
from django.contrib.auth.forms import UserCreationForm
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
    pass



class CustomRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')

    def form_invalid(self, form):
        user = form.save()
        user_group, created = Group.objects.get_or_create(name='Usuario')
        user.groups.add(user_group)
        login(self.request, user)
        return super().form_valid(form)
