from django.shortcuts import render, reverse, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django import views


from typing import Optional

from .forms import UserLoginForm, UserRegistrationForm


class LLDLoginView(views.View):
    """View for handling user login."""

    template_name: str = "accounts/login.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET requests to the login page.

        Renders the login form for users to enter their credentials.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            HttpResponse: The response containing the login form template.
        """
        form = UserLoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handle POST requests to the login page.

        Validates the user's login credentials, logs the user in if valid,
        or renders the login form again with errors if invalid.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            HttpResponse: The response after processing the login form submission.
        """
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
        else:
            return render(request, self.template_name, {"form": form})


class LLDRegisterView(views.View):
    """View for handling user registration."""

    template_name: str = "accounts/register.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET requests to the registration page.

        Renders the registration form for users to sign up.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            HttpResponse: The response containing the registration form template.
        """
        form = UserRegistrationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handle POST requests to the registration page.

        Validates the user's registration data, creates a new user account if valid,
        logs the user in, and then redirects to the appropriate page.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            HttpResponse: The response after processing the registration form submission.
        """
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            _handle_redirect(request, default_next="home")
        else:
            return render(request, self.template_name, {"form": form})


def _handle_redirect(
    request: HttpRequest, default_next: Optional[str] = "home"
) -> HttpResponse:
    """Handle redirection after login or registration.

    If a referrer URL is present in the session, the user will be redirected
    back to that URL after login or registration. Otherwise, the user will be
    redirected to the default URL specified.

    Args:
        request (HttpRequest): The incoming request.
        default_next (str, optional): The default URL name to redirect to if
            no referrer URL is found in the session. Defaults to "home".

    Returns:
        HttpResponse: The redirection response.
    """
    referrer_url = request.session.pop("referrer_url", None)

    if referrer_url:
        return redirect(referrer_url)

    return redirect(reverse(default_next))
