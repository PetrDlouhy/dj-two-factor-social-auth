import django_otp
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import FormView
from two_factor.forms import AuthenticationTokenForm
from two_factor.utils import default_device


class AuthenticationView(FormView):
    template_name = "two_factor/core/login.html"
    form_class = AuthenticationTokenForm

    def get_success_url(self):
        self.request.session["tfa_completed"] = True
        django_otp.login(self.request, self.device)
        return reverse(
            "social:complete",
            kwargs={"backend": self.request.session.get("tfa_social_backend")},
        )

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        user_id = self.request.session.get("tfa_social_user_id")
        if not user_id:
            raise ValueError("No user found in session")
        user = get_user_model().objects.get(id=user_id)
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
