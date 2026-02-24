from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from disposable_emails.contrib.django import disposable_validator
from django.contrib.auth import authenticate
from .models import * # tu modelo custom

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
    username = forms.CharField(label="Usuario/email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))


    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            if '@' in username:
                user= User.objects.filter(username__iexact=username)
                username = user[0].username
        except Usuario.DoesNotExist:
            raise forms.ValidationError("unregistered email")


        self.user_cache= authenticate(self.request, username=username, password=password)
        if self.user_cache is None:
            return forms.ValidationError("Incorrect username or password")
        return self.cleaned_data






