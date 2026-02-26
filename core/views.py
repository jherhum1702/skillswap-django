from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from .forms import *
from django.views.decorators.http import require_http_methods

# Create your views here.

class HomeView(ListView):
    """
    Display a paginated list of publications with optional search filtering.

    Parameters
    ----------
    model : Publicacion
        The model used to retrieve the list of posts.
    context_object_name : str
        Name of the variable passed to the template containing the posts.
    paginate_by : int
        Number of posts per page.
    ordering : tuple
        Default ordering for the queryset.

    Notes
    -----
    The search query (``q``) supports filtering by:

    - ``BUSCO`` or ``OFREZCO`` to filter by post type.
    - Any other term to filter by skill name or description.

    If a query is present, renders ``core/post_list.html``, otherwise ``core/home.html``.

    Examples
    --------
    URL config::

        path('', HomeView.as_view(), name='home')

    Template usage::

        {% for post in posts %}
            {{ post.habilidad.nombre }}
        {% endfor %}

    Search examples::

        /?q=ajedrez         → posts with skill "Ajedrez"
        /?q=busco ajedrez   → posts of type BUSCO with skill "Ajedrez"
        /?q=ofrezco python  → posts of type OFREZCO with skill "Python"
    """
    context_object_name = 'posts'
    model = Publicacion
    paginate_by = 10
    ordering = ('-fecha_modificacion',)

    def get_template_names(self):
        if self.request.GET.get('q'):
            return ['core/post_list.html']
        return ['core/home.html']

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '').strip()

        if q:
            tipo_filter = None
            search_terms = []

            for word in q.split():
                word_upper = word.upper()
                if word_upper in ['BUSCO', 'OFREZCO']:
                    tipo_filter = word_upper
                else:
                    search_terms.append(word)

            if tipo_filter:
                queryset = queryset.filter(tipo=tipo_filter)

            for term in search_terms:
                queryset = queryset.filter(
                    Q(habilidad__nombre__icontains=term) |
                    Q(descripcion__icontains=term)
                )

        return queryset.distinct().select_related('autor', 'autor__perfil', 'habilidad').prefetch_related('autor__perfil__habilidades')

class Postlistview(ListView):
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
    template_name = 'core/post_list.html'
    context_object_name = 'posts'


class PostDetailview(DetailView):
    model = Publicacion
    template_name = 'core/post_detail.html'
    context_object_name = 'post'


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

@require_http_methods(["POST"])
def change_preference(request):
    """
    Change user preferences for theme and language based on POST
    data and store them in cookies.

    Parameters
    ----------
    request : HttpRequest
        The request object contining POST data
        - theme: 'light' or 'dark' (default: 'light')
        - lang: 'es' or 'en' (default: 'es')

    Returns
    -------
    POST /cambiar-preferencia/ with data:
        {
            'theme': 'dark',
            'lang': 'en'
        }
    """
    theme = request.POST.get('theme')
    lang = request.POST.get('lang')

    redirect_url = request.META.get('HTTP_REFERER', reverse_lazy('core:home'))

    response = redirect(redirect_url)

    if theme:
        response.set_cookie('theme', theme, max_age=365*24*60*60)
    if lang:
        response.set_cookie('lang', lang, max_age=365*24*60*60)

    return response