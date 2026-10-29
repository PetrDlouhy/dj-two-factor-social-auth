.. :changelog:

History
-------

1.0.4 (unreleased)
++++++++++++++++++

- Nothing changed yet.


1.0.3 (2026-10-29)
++++++++++++++++++

* Security fix: the session flag recording a completed 2FA step was never
  cleared and was not tied to the user who completed it, so a session that had
  passed 2FA once could finish a social login as another account without that
  account's OTP step. The flag is now bound to the user and to the challenged
  partial pipeline, and is consumed on the next pass of the pipeline step.
* Fix: the OTP page answered 500 when no social login was waiting for it
  (a refreshed tab, the back button, an expired login). It now redirects to
  ``LOGIN_URL``.
* Tested on Django 6.0 and 6.1, Python 3.14 and 3.15, and
  social-auth-app-django 7


1.0.2 (2026-08-27)
++++++++++++++++++

* Fix: take the session from the strategy instead of the pipeline's ``request``
  keyword argument, which social-auth-core 5.x overwrites with the request data
  when it resumes a partial pipeline (breaking the OTP round trip)

1.0.1 (2025-05-19)
++++++++++++++++++

* Fix: session transfer of data

1.0.0 (2025-05-15)
++++++++++++++++++

* Use session to transfer data (safer, more reliable)
* Update support up to Django 5.2, Python 3.13 versions
* Drop support for Python 3.8, Django 4.0 and below

0.1.2 (2023-03-09)
++++++++++++++++++

* Try to rename package to be compatible with poetry (https://github.com/python-poetry/poetry/issues/6996)

0.1.1 (2023-03-08)
++++++++++++++++++

* Update testing and setup.py to support newest Django, Python and django-two-factor-auth

0.1.0 (2022-03-21)
++++++++++++++++++

* First release on PyPI.
