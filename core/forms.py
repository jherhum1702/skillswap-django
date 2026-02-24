from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from disposable_emails.contrib.django import disposable_validator
from django.contrib.auth import authenticate
from .models import * # tu modelo custom
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ("username","alias" ,"email",)
        widgets = {
            'username': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter the username ',
                'pattern':'^[a-zA-Z0-9_]+$',
                'required':True,
            }),
            'email': forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your email address',
                'required': True,
            }),
            'alias': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your Nickname',
                'pattern':'^[a-zA-Z0-9_]+$',
                'required': True,
            }),
            'password1': forms.PasswordInput(attrs={
                'class':'form-control form-control-sm',
                'placeholder':'Enter your Password',
            }),
            'password2': forms.PasswordInput(attrs={
                'class':'form-control form-control-sm',
                'placeholder':'Enter your Password',
            })
        }
    email = forms.EmailField(validators=[disposable_validator]) #teporal email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if hasattr(user, 'alias'):
            user.alias = self.cleaned_data['alias']
        if commit:
            user.save()
            self.save_m2m()
        return user


class CustomloginForm(AuthenticationForm):
    username = forms.CharField(label="Alias/Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            # Login por alias O email
            if '@' in username:
                user = Usuario.objects.get(email__iexact=username)
            else:
                user = Usuario.objects.get(alias__iexact=username)  # ← ALIAS!
            username = user.username  # convierte a username

        except Usuario.DoesNotExist:
            raise forms.ValidationError("Alias/Email no registrado")

        self.user_cache = authenticate(self.request, username=username, password=password)

        if self.user_cache is None:
            raise forms.ValidationError("Alias/Email o contraseña incorrectos")

        self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

# MiClaveSegura2026!
