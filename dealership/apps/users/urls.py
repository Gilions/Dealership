from django.urls import path

from . import views

urlpatterns = [
    # Регистрация на сайте.
    path("signup/", views.SignUp.as_view(), name="signup")
]
