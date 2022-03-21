import django_otp
from django.urls import reverse
from django.views.generic import FormView
from social_django.utils import load_strategy
from two_factor.forms import AuthenticationTokenForm
from two_factor.utils import default_device


class AuthenticationView(FormView):
    template_name = "two_factor/core/login.html"
    form_class = AuthenticationTokenForm

    def get_success_url(self):
        partial = self.get_partial()
        self.request.session["tfa_completed"] = True
        self.request.user = self.get_partial().kwargs["user"]
        django_otp.login(self.request, self.device)
        return (
            reverse("social:complete", kwargs={"backend": partial.backend})
            + f"?partial_token={partial.token}"
        )

    def get_partial(self):
        strategy = load_strategy()
        partial_token = self.request.GET.get("partial_token")
        partial = strategy.partial_load(partial_token)
        return partial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        user = self.get_partial().kwargs["user"]
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
