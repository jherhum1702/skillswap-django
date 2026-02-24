import email

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import authenticate
from .models import * # tu modelo custom
import requests as req

# EMAIL BLOCK LIST
lista = req.get("https://gist.githubusercontent.com/ammarshah/f5c2624d767f91a7cbdc4e54db8dd0bf/raw")
contenido = lista.text
lista_email_block = set(contenido.split("\n"))
lista_email_block.add('pazuric.com')




class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''

        self.fields['password1'].widget.attrs.update({
            'class':'form-control',
            'pattern':'^[a-zA-Z0-9_]+$',
            'required':True,
            'placeholder':'Enter your Password',
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'pattern': '^[a-zA-Z0-9_]+$',
            'required': True,
            'placeholder': 'Enter your Password',
        })





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
        }
    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('@')[1]

        if domain in lista_email_block:
            raise forms.ValidationError("this email is not valid")

        return email

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


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class':'form-control',
            'required':True,
            'placeholder':'Enter the alias or email',
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'required': True,
            'placeholder': 'Enter your Password',
        })


    username = forms.CharField(label="Alias/Email")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)

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
