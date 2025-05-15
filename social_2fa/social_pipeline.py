from django.shortcuts import redirect
from django.urls import reverse
from social_core.pipeline.partial import partial
from two_factor.utils import default_device


@partial
def two_factor_auth(strategy, details, *args, user=None, **kwargs):
    current_partial = kwargs.get("current_partial")
    request = kwargs["request"]
    if request.session.get("tfa_completed", False):
        return details
    if default_device(user):
        request.session["tfa_social_user_id"] = user.id
        request.session["tfa_social_backend"] = current_partial.backend
        return redirect(reverse("social_2fa:two_factor_authentication"))
    return details
