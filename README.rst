=============================
Django two factor auth for Django social auth
=============================

.. image:: https://badge.fury.io/py/dj-2fa-social-auth.svg
    :target: https://badge.fury.io/py/dj-2fa-social-auth

.. image:: https://travis-ci.org/PetrDlouhy/dj-2fa-social-auth.svg?branch=master
    :target: https://travis-ci.org/PetrDlouhy/dj-2fa-social-auth

.. image:: https://codecov.io/gh/PetrDlouhy/dj-2fa-social-auth/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/PetrDlouhy/dj-2fa-social-auth

App connecting django-two-factor-auth and django-social-auth. If user authenticates through social auth, he will be enforced to go through 2FA (if he has it enabled).

Documentation
-------------

The full documentation is at https://dj-2fa-social-auth.readthedocs.io.

Quickstart
----------

Install Django two factor auth for Django social auth::

    pip install dj-2fa-social-auth

Add it to your `INSTALLED_APPS`:

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

Features
--------

* TODO

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


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
