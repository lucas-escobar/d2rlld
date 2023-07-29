from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordResetForm,
    PasswordChangeForm,
    SetPasswordForm,
)

from .models import LLDUser


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = LLDUser
        fields = ["email", "password1", "password2"]


class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)
