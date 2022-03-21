=====
Usage
=====

To use Django two factor auth for Django social auth in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'social_2fa.apps.Social2faConfig',
        ...
    )

Add Django two factor auth for Django social auth's URL patterns:

.. code-block:: python

    from social_2fa import urls as social_2fa_urls


    urlpatterns = [
        ...
        url(r'^', include(social_2fa_urls)),
        ...
    ]
