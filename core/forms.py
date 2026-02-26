import email

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import authenticate
from .models import *
from disposable_email_domains import blocklist






class CustomUserCreationForm(UserCreationForm):
    """
    Custom registration form for the SkillSwap platform.

    Extends Django's UserCreationForm to support the custom Usuario model,
    adding alias field, email domain validation against a blocklist,
    and Bootstrap styling for all fields.

    Attributes:
        fields (tuple): Includes username, alias, and email.
        lista_email_block (set): Set of blocked email domains loaded at module level.

    Methods:
        clean_email: Validates that the email domain is not in the blocklist.
        save: Persists email and alias fields to the Usuario model.

    Example:
        >>> form = CustomUserCreationForm(data={
        ...     'username': 'john_doe',
        ...     'email': 'john@gmail.com',
        ...     'password1': 'SecurePass123',
        ...     'password2': 'SecurePass123',
        ... })
        >>> if form.is_valid():
        ...     user = form.save()
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the form, removing help texts and applying Bootstrap styling.

        Clears all default Django help texts for a cleaner UI, and applies
        Bootstrap 'form-control' class and placeholders to the password fields,
        since these cannot be styled via the Meta widgets dict.

        Args:
            *args: Variable length argument list passed to parent constructor.
            **kwargs: Arbitrary keyword arguments passed to parent constructor.

        Example:
            >>> form = CustomUserCreationForm()
            >>> form.fields['password1'].widget.attrs['class']
            'form-control'
        """

        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''

        self.fields['password1'].widget.attrs.update({
            'class':'form-control',
            'required':True,
            'placeholder':'Enter your Password',
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'required': True,
            'placeholder': 'Enter your Password',
        })

    class Meta:
        """
        Metaclass configuration for CustomUserCreationForm.

        Binds the form to the Usuario model and defines the fields
        to display along with their Bootstrap-styled widgets.

        Attributes:
            model (Usuario): The custom user model for SkillSwap.
            fields (tuple): Fields exposed in the form: username, alias, and email.
            widgets (dict): Custom widget configuration for each field,
                            applying Bootstrap 'form-control' styling and
                            HTML5 validation patterns.

        Note:
            password1 and password2 are intentionally excluded here since
            they are not model fields and must be styled via __init__ instead.
        """
        model = Usuario
        fields = ("username",'first_name','last_name',"email")
        widgets = {
            'first_name': forms.TextInput(attrs={
               'class':'form-control',
                'placeholder':'Enter your first name',
                'required': True,
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name',
                'required': True,
            }),
            'username': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your username',
                'pattern':'^[a-zA-Z0-9_]+$',
                'required':True,
            }),
            'email': forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your email address',
                'required': True,
            }),
        }



    def clean_email(self):
        """
        Validate that the email domain is not in the blocklist.

        Extracts the domain from the submitted email and checks it
        against the globally loaded set of blocked disposable email domains.

        Args:
            self: Form instance with cleaned_data available.

        Returns:
            str: The validated email address if domain is allowed.

        Raises:
            ValidationError: If the email domain is found in the blocklist.

        Example:
            >>> form = CustomUserCreationForm(data={..., 'email': 'user@mailinator.com'})
            >>> form.is_valid()
            False
            >>> form.errors['email']
            ['this email is not valid']
        """
        email = self.cleaned_data['email']
        domain = email.split('@')[1]
        if domain in blocklist:
            raise forms.ValidationError("This email is not valid")
        return email



    def save(self, commit=True):
        """
        Save the form data to the Usuario model instance.

        Extends the default save to explicitly persist the email and alias
        fields, since these are custom fields not handled automatically
        by UserCreationForm.

        Args:
            commit (bool): If True, saves the user to the database immediately.
                           If False, returns an unsaved model instance.
                           Defaults to True.

        Returns:
            Usuario: The saved (or unsaved) user instance.

        Example:
            >>> form = CustomUserCreationForm(data={...})
            >>> if form.is_valid():
            ...     user = form.save()              # saves to DB
            ...     user = form.save(commit=False)  # returns unsaved instance
        """
        user = super().save(commit=False)
        user.username = self.cleaned_data['username'].lower()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user







class CustomloginForm(AuthenticationForm):

    """
    Custom login form for the SkillSwap platform.

    Extends Django's AuthenticationForm to allow users to log in
    using either their email address or alias, instead of just username.
    Includes Bootstrap styling for all fields.

    Attributes:
        username (CharField): Accepts either an alias or email address.
        password (CharField): User's password.

    Methods:
        clean: Resolves the alias or email to a valid username,
               then authenticates the user against Django's auth backend.

    Raises:
        ValidationError: If the alias/email is not registered,
                         or if the password is incorrect.

    Example:
        >>> form = CustomloginForm(data={
        ...     'username': 'johnny',
        ...     'password': 'SecurePass123',
        ... })
        >>> if form.is_valid():
        ...     user = form.get_user()
    """


    def __init__(self, *args, **kwargs):
        """
        Initialize the login form with Bootstrap styling.

        Applies Bootstrap 'form-control' class and placeholders to the
        username and password fields inherited from AuthenticationForm.

        Args:
            *args: Variable length argument list passed to parent constructor.
            **kwargs: Arbitrary keyword arguments passed to parent constructor.

        Example:
            >>> form = CustomloginForm()
            >>> form.fields['username'].widget.attrs['placeholder']
            'Enter the alias or email'
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class':'form-control',
            'required':True,
            'placeholder':'Enter the usernmae or email',
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'required': True,
            'placeholder': 'Enter your Password',
        })


    username = forms.CharField(label="Username/Email")
    password = forms.CharField(label="ContraseÃ±a", widget=forms.PasswordInput, required=True)

    def clean(self):
        """
        Validate credentials allowing login via alias or email.

        Resolves the submitted username field to an actual Usuario instance
        by checking if it contains '@' (email) or not (alias), then
        authenticates against Django's auth backend.

        Returns:
            dict: The cleaned form data if authentication succeeds.

        Raises:
            ValidationError: If the alias/email is not registered in the system.
            ValidationError: If the password does not match the found user.

        Example:
            >>> form = CustomloginForm(data={
            ...     'username': 'johnny',         # login via alias
            ...     'password': 'SecurePass123',
            ... })
            >>> form = CustomloginForm(data={
            ...     'username': 'john@gmail.com', # login via email
            ...     'password': 'SecurePass123',
            ... })
            >>> if form.is_valid():
            ...     user = form.get_user()
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            if '@' in username:
                user = Usuario.objects.get(email__iexact=username)
            else:
                user = Usuario.objects.get(username__iexact=username)
            username = user.username

        except Usuario.DoesNotExist:
            raise forms.ValidationError("Username/Email no registrado")

        self.user_cache = authenticate(self.request, username=username, password=password)

        if self.user_cache is None:
            raise forms.ValidationError("Incorrect Username/Email or password")

        self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

class ProfileForm(forms.ModelForm):
    def init(self, args, **kwargs):
        super().init(args, **kwargs)
        if self.instance.pk:
            habilidades_actuales = self.instance.habilidades.values_list('nombre', flat=True)  # â† .values_list() no ()
            self.fields['habilidades_nuevas'].initial = ', '.join(habilidades_actuales)  # â† sin .nombre

    habilidades_nuevas = forms.CharField(
        required=False,
        label="Habilidades",
        help_text="Escribe habilidades separadas por comas"
    )

    class Meta:
        model = Perfil
        fields = ['biografia', 'zona_horaria', 'disponibilidad' ]
        widgets = {
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'zona_horaria': forms.Select(attrs={'class': 'form-select'}),
            'disponibilidad': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def save(self, commit=True):
        profile = super().save(commit=commit)
        nuevas = self.cleaned_data['habilidadesnuevas']
        if nuevas:
            habilidades = []
            for n in nuevas.split(','):
                nombre = n.strip().lower().capitalize()  # "python" y "Python" â†’ "Python"
                if nombre:
                    habilidad,  = Habilidad.objects.get_or_create(
                        nombre__iexact=nombre,
                        defaults={'nombre': nombre}
                    )
                    habilidades.append(habilidad)
            profile.habilidades.set(habilidades)
        return profile