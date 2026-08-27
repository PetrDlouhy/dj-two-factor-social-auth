from django.shortcuts import redirect
from django.urls import reverse
from social_core.pipeline.partial import partial
from two_factor.utils import default_device


@partial
def two_factor_auth(strategy, details, *args, user=None, **kwargs):
    # The session is read through the strategy rather than through the
    # pipeline's ``request`` keyword argument: when social-core resumes a
    # partial pipeline - which is exactly the pass that follows the OTP step -
    # ``_extend_partial_pipeline`` sets that argument to the request *data*,
    # which has no session.
    current_partial = kwargs.get("current_partial")
    if strategy.session_get("tfa_completed", False):
        return details
    if default_device(user):
        strategy.session_set("tfa_partial_token", current_partial.token)
        return redirect(reverse("social_2fa:two_factor_authentication"))
    return details
