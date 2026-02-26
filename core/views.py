
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from .forms import *
from .models import *

# Create your views here.

class Postview(ListView):
    """
    Display a paginated list of all publications.

    Parameters
    ----------
    model : Publicacion
        The model used to retrieve the list of posts.
    template_name : str
        Path to the template used to render the list.
    context_object_name : str
        Name of the variable passed to the template containing the posts.

    Examples
    --------
    URL config::

        path('', Postview.as_view(), name='home')

    Template usage::

        {% for post in posts %}
            {{ post.titulo }}
        {% endfor %}
    """
    model = Publicacion
    template_name = 'core/publicacion_list.html'
    context_object_name = 'posts'




class CustomLogin(LoginView):
    """
    Custom login view for the SkillSwap platform.

    Parameters
    ----------
    form_class : CustomloginForm
        Custom form that allows login via alias or email.
    template_name : str
        Path to the template used to render the login form.

    Methods
    -------
    get_success_url()
        Returns the URL to redirect to after a successful login.

    Examples
    --------
    URL config::

    path('accounts/login/', CustomLogin.as_view(), name='login'),

    Template usage::

        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Iniciar sesión</button>
        </form>
    """
    form_class = CustomloginForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        """
        Return the URL to redirect to after successful login.

        Returns
        -------
        str
            Resolved URL for the SkillSwap home page.

        Examples
        --------
        >>> view = CustomLogin()
        >>> view.get_success_url()
        '/home/'
        """
        return reverse_lazy('core:home')



class CustomRegisterView(CreateView):
    """
    Custom registration view for the SkillSwap platform.

    Parameters
    ----------
    form_class : CustomUserCreationForm
        Custom form that handles user registration with alias and email validation.
    template_name : str
        Path to the template used to render the registration form.
    success_url : str
        URL to redirect to after successful registration.

    Methods
    -------
    form_valid(form)
        Saves the user, assigns them to the 'Usuario' group, and logs them in.

    Examples
    --------
    URL config::

        path('accounts/register/', CustomRegisterView.as_view(), name='registro'),

    Template usage::

        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Registrarse</button>
        </form>
    """
    form_class = CustomUserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        """
        Handle valid form submission.

        Saves the new user, assigns them to the default 'Usuario' group,
        and automatically logs them in after registration.

        Parameters
        ----------
        form : CustomUserCreationForm
            The validated registration form instance.

        Returns
        -------
        HttpResponseRedirect
            Redirects to success_url after saving and logging in the user.

        Examples
        --------
        >>> view = CustomRegisterView()
        >>> response = view.form_valid(valid_form)
        >>> response.status_code
        302
        """
        user = form.save()
        Perfil.objects.create(usuario=user)
        user_group, created = Group.objects.get_or_create(name='Usuario')
        user.groups.add(user_group)
        login(self.request, user)
        return super().form_valid(form)



class ProfileView(DetailView):
    model = Perfil
    template_name = 'core/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.perfil

class ProfileUpdateView(UpdateView):
    model = Perfil
    form_class = ProfileForm
    template_name = 'core/profile_update.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.perfil

    def get_success_url(self):
        return reverse_lazy('core:profile')