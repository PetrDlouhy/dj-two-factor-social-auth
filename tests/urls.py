# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.urls import path, include
from django.contrib import admin
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_2fa.urls', namespace='social_2fa')),
    path("", include("social_django.urls", namespace="social")),
    path('', include(tf_urls)),
]
