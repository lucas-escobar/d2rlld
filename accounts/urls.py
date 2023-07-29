from django.urls import path, include

from .views import LLDLoginView, LLDRegisterView

app_name = "accounts"

urlpatterns = [
    path("login/", LLDLoginView.as_view(), name="login"),
    path("register/", LLDRegisterView.as_view(), name="register"),
]
