import django_otp
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView
from social_django.utils import load_strategy
from two_factor.forms import AuthenticationTokenForm
from two_factor.utils import default_device

from .social_pipeline import tfa_completed_marker


class AuthenticationView(FormView):
    template_name = "two_factor/core/login.html"
    form_class = AuthenticationTokenForm

    def dispatch(self, request, *args, **kwargs):
        # The social login that asked for the OTP is no longer pending (done,
        # expired, or never started), so there is no one to challenge.
        if self.get_partial() is None:
            return redirect(settings.LOGIN_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_user(self):
        partial = self.get_partial()
        user = partial.kwargs["user"]
        if not user:
            raise ValueError("No user found")
        return user

    def get_success_url(self):
        partial = self.get_partial()
        user = self.get_user()
        self.request.session["tfa_completed"] = tfa_completed_marker(
            user, partial.token
        )
        self.request.user = user
        django_otp.login(self.request, self.device)
        return reverse("social:complete", kwargs={"backend": partial.backend})

    def get_partial(self):
        strategy = load_strategy()
        partial_token = self.request.session.get("tfa_partial_token")
        partial = strategy.partial_load(partial_token)
        return partial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        user = self.get_user()
        kwargs["user"] = user
        self.device = default_device(user)
        kwargs["initial_device"] = self.device
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wizard"] = {
            "steps": {"current": "token"},
            "form": context["form"],
        }
        return context
