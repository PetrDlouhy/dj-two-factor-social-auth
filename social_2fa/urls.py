from django.urls import path

from . import views

urlpatterns = [
    path(
        "two-factor-social-auth/",
        views.AuthenticationView.as_view(),
        name="two_factor_authentication",
    ),
]

app_name = "social_2fa"
