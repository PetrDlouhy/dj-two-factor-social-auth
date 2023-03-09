=============================================
Django two factor auth for Django social auth
=============================================

.. image:: https://badge.fury.io/py/dj-two-factor-social-auth.svg
    :target: https://badge.fury.io/py/dj-two-factor-social-auth

.. image:: https://codecov.io/gh/PetrDlouhy/dj-two-factor-social-auth/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/PetrDlouhy/dj-two-factor-social-auth

App connecting `django-two-factor-auth <https://github.com/jazzband/django-two-factor-auth>`_ and `social-app-django <https://github.com/python-social-auth/social-app-django>`_. If user authenticates through social auth, he will be enforced to go through 2FA (if he has 2FA enabled).

Documentation
-------------

The full documentation is at https://dj-two-factor-social-auth.readthedocs.io.

Quickstart
----------

We expect, that you have already installed and configured `django-two-factor-auth <https://github.com/jazzband/django-two-factor-auth>`_ and `social-app-django <https://github.com/python-social-auth/social-app-django>`_ according to their documentation.

Install Django two factor auth for Django social auth::

    pip install dj-two-factor-social-auth

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        "two_factor",
        "social_django",
        "social_2fa",
        ...
    )

Add Django two factor auth for Django social auth's URL patterns:

.. code-block:: python

    from django.urls import path
    
    
    urlpatterns = [
        ...
        path("", include("social_2fa.urls")),
        ...
    ]

Add social_2fa to your social pipeline in ``settings.py``:


.. code-block:: python

    SOCIAL_AUTH_PIPELINE = (
        ...
        "social_2fa.social_pipeline.two_factor_auth",
    )

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l
