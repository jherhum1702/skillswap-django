from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.contrib.sessions.models import Session
from django.db.models import Q, Count, Case, When, IntegerField, F
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, TemplateView, DeleteView
from .forms import *
from django.views.decorators.http import require_http_methods
from .session_manager import SessionManager

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
        q = self.request.GET.get('q', '').strip()
        if not q:
            # Check if there are saved filters in session
            filters = SessionManager.get_filters(self.request)
            q = filters.get('q', '')

        if q:
            return ['core/search_results.html']
        return ['core/home.html']

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '').strip()

        # If no search in URL, try to restore from session
        if not q:
            filters = SessionManager.get_filters(self.request)
            q = filters.get('q', '')
        else:
            # If new search, save to session
            SessionManager.save_filters(self.request, q=q)

        # If no query at all, clear filters
        if not q:
            SessionManager.clear_filters(self.request)

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

    def get_context_data(self, **kwargs):
        """
        Add saved filters to the template context.

        Returns the context with filters recovered from session so the template can display the active search filters.
        """

        context = super().get_context_data(**kwargs)
        filters = SessionManager.get_filters(self.request)
        context['filters'] = filters
        return context

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

    def get_object(self, queryset=None):
        return Publicacion.objects.annotate(total_proposals=Count('acuerdo', filter=Q(acuerdo__estado='PROPUESTO'))).get(pk=self.kwargs['pk'])

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

def clear_filters(request):
    """
    Clear all search filters from the session.

    Removes the saved search filters and redirects back to home.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object containing the session.

    Returns
    -------
    HttpResponseRedirect
        Redirects to the home page with filters cleared.

    Examples
    --------
    URL config::

        path('clear-filters/', clear_filters, name='clear_filters'),
    """
    SessionManager.clear_filters(request)
    return redirect(reverse_lazy('core:home'))

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



class StatisticsView(TemplateView):
    template_name = 'core/statistics.html'

    def get_context_data(self, **kwargs):
        context = super(StatisticsView, self).get_context_data(**kwargs)
        context['total_posts'] = Publicacion.objects.count()
        context['ongoing_agreements'] = Acuerdo.objects.filter(estado='EN CURSO').count()
        context['total_agreements'] = Acuerdo.objects.count()
        context['finished_agreements'] = Acuerdo.objects.filter(estado__exact='FINALIZADO').count()
        context['proposed_agreements'] = Acuerdo.objects.filter(estado__exact='PROPUESTO').count()
        context['canceled_agreements'] = Acuerdo.objects.filter(estado__exact='CANCELADO').count()
        context['accepted_agreements'] = Acuerdo.objects.filter(estado__exact='ACEPTADO').count()
        context['skills'] = Habilidad.objects.filter(publicacion__tipo='OFREZCO').distinct().count()
        context['registered_users'] = Usuario.objects.filter(groups__exact='1').count()
        context['total_sessions'] = Sesion.objects.count()
        context['active_sessions'] = Sesion.objects.filter(estado=True).count()
        context['finished_sessions'] = Sesion.objects.filter(estado=False).count()
        context['moderators'] = Usuario.objects.filter(groups__name__exact='Moderador')
        context['recent_posts'] = Publicacion.objects.order_by('-fecha_creacion')[:10]
        context['recent_ofrezco'] = Publicacion.objects.filter(tipo='OFREZCO').order_by('-fecha_creacion')[:10]
        context['recent_busco'] = Publicacion.objects.filter(tipo='BUSCO').order_by('-fecha_creacion')[:10]
        context['posts_ofrezco'] = Publicacion.objects.filter(tipo='OFREZCO').count()
        context['posts_busco'] = Publicacion.objects.filter(tipo='BUSCO').count()
        context['actividad_reciente'] = Acuerdo.objects.select_related('usuario_a', 'usuario_b').order_by('-id')[:10] # There isn't any date field, had to use -id.

        return context


class DealsCreateView(CreateView):
    model = Acuerdo
    form_class = DealsPost
    template_name = 'core/dealsCreate.html'
    success_url = reverse_lazy('core:home')

    def get_usuario_a(self):
        return get_object_or_404(Usuario, pk=self.request.GET.get('autor'))

    def get_publicacion(self):
        return get_object_or_404(Publicacion, pk=self.request.GET.get('post'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario_a'] = self.get_usuario_a()
        kwargs['usuario_b'] = self.request.user
        kwargs['publicacion'] = self.get_publicacion()
        return kwargs

    def form_valid(self, form):
        acuerdo = form.save(commit=False)
        acuerdo.usuario_a = self.get_usuario_a()
        acuerdo.usuario_b = self.request.user
        acuerdo.habilidad_tradea_a = self.get_publicacion().habilidad
        acuerdo.publicacion = self.get_publicacion()  # ← añadir esto
        try:
            acuerdo.save()
        except IntegrityError:
            messages.error(self.request, 'Ya tienes un acuerdo activo con esta persona para estas habilidades.')
            return self.form_invalid(form)
        return redirect('core:home')

    def form_invalid(self, form):
        for error in form.non_field_errors():
            messages.error(self.request, error)
        return super().form_invalid(form)







class DealsUpdateAccepView(View):
    def post(self, request, pk):
        acuerdo = get_object_or_404(Acuerdo, pk=pk)
        if request.user == acuerdo.usuario_b:
            messages.error(request, 'No puedes aceptar un acuerdo que tú mismo has propuesto.')
            return redirect('core:deals-detail', pk=pk)
        acuerdo.estado = 'ACEPTADO'
        acuerdo.save()
        return redirect('core:deals')

class DealsUpdateCancelView(View):
    def post(self, request, pk):
        acuerdo = get_object_or_404(Acuerdo, pk=pk)
        acuerdo.estado = 'CANCELADO'
        acuerdo.save()
        return redirect('core:deals')

class DealsUpdateFinView(View):
    def post(self, request, pk):
        acuerdo = get_object_or_404(Acuerdo, pk=pk)
        acuerdo.estado = 'FINALIZADO'
        acuerdo.save()
        return redirect('core:deals')
class DealsUpdateStartView(View):
    def post(self, request, pk):
        acuerdo = get_object_or_404(Acuerdo, pk=pk)
        acuerdo.estado = 'EN CURSO'
        acuerdo.save()
        return redirect('core:deals')




class DealsDeleteView(DeleteView):
    pass


class DealsDetailView(DetailView):
    model = Acuerdo
    context_object_name = 'deal'
    template_name = 'core/dealsDetail.html'
    success_url = reverse_lazy('core:deals')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estado'] = 'Activa' if self.object.estado else 'Cerrada'
        context['total_proposals'] = Acuerdo.objects.filter(usuario_a=self.object.autor,estado='PROPUESTO').count()
        return context


class DealsListView(ListView):
    model = Acuerdo
    context_object_name = 'deals'
    template_name = 'core/dealslist.html'

    def get_queryset(self):
        return Acuerdo.objects.filter(models.Q(usuario_a=self.request.user) | models.Q(usuario_b=self.request.user)).annotate(
            orden=Case(
                When(estado='EN CURSO', then=0),
                When(estado='ACEPTADO', then=1),
                When(estado='PROPUESTO', then=2),
                When(estado='CANCELADO', then=3),
                When(estado='FINALIZADO', then=4),
                default=5, output_field=IntegerField(),)).order_by('orden') # I do this because of annotate requirement, as I was going to do multiple queries and order them.


class PostCreateview(CreateView):
    model = Publicacion
    form_class = PostCreate
    success_url = reverse_lazy('core:post')
    template_name = 'core/postCreate.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mis_habilidades'] = list(
            self.request.user.perfil.habilidades.values_list('id', flat=True)
        )
        return context





class PostUpdateView(UpdateView):
    model = Publicacion
    form_class = PostCreate
    context_object_name = 'post'
    success_url = reverse_lazy('core:post')
    template_name = 'core/post_update.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mis_habilidades'] = list(
            self.request.user.perfil.habilidades.values_list('id', flat=True)
        )
        return context

class PostCloseView( View):
    def post(self, request, pk):
        publicacion = get_object_or_404(Publicacion, pk=pk, autor=request.user)
        publicacion.estado = False
        publicacion.save()
        return redirect('core:post')