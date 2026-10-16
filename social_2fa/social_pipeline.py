from django.shortcuts import redirect
from django.urls import reverse
from social_core.pipeline.partial import partial
from two_factor.utils import default_device


def tfa_completed_marker(user, partial_token):
    """Session value recording that ``user`` passed 2FA for the partial ``partial_token``."""
    return {"user": str(user.pk), "partial_token": partial_token}


@partial
def two_factor_auth(
    strategy, details, *args, user=None, tfa_partial_token=None, **kwargs
):
    """Halt the pipeline for the OTP step if the user has a 2FA device.

    The challenge records its partial token in the partial itself
    (``tfa_partial_token``), so only the resume of that partial matches the
    marker the OTP view stores. The marker is popped on every pass.
    """
    # The session is read through the strategy rather than through the
    # pipeline's ``request`` keyword argument: when social-core resumes a
    # partial pipeline - which is exactly the pass that follows the OTP step -
    # ``_extend_partial_pipeline`` sets that argument to the request *data*,
    # which has no session.
    current_partial = kwargs.get("current_partial")
    completed = strategy.session_pop("tfa_completed")
    if not default_device(user):
        return details
    if completed == tfa_completed_marker(user, tfa_partial_token):
        return details
    current_partial.extend_kwargs({"tfa_partial_token": current_partial.token})
    strategy.session_set("tfa_partial_token", current_partial.token)
    return redirect(reverse("social_2fa:two_factor_authentication"))
