import random

from django.test import RequestFactory, TestCase
from model_bakery import baker
from social_core.backends.google import GoogleOAuth2
from social_core.storage import BaseStorage
from social_core.tests.strategy import TestStrategy

from .. import social_pipeline


class PipelineTests(TestCase):
    def setUp(self):
        random.seed(1)
        self.user = baker.make("User")
        storage = BaseStorage()
        storage.partial = baker.make(
            "Partial",
            token="foo",
            kwargs={"user": self.user.id},
        )
        self.strategy = TestStrategy(storage=storage)
        factory = RequestFactory()
        self.request = factory.get("/")
        self.request.user = self.user
        self.request.session = self.client.session
        self.backend = GoogleOAuth2()

    def test_pipeline(self):
        """Complete pipeline if no device is set"""
        ret = social_pipeline.two_factor_auth(
            self.strategy,
            backend=self.backend,
            details="details",
            pipeline_index=11,
            user=self.user,
            request=self.request,
        )
        self.assertEqual(ret, "details")

    def test_pipeline_with_device_tfa_completed(self):
        """If two factor authentication is completed, don't redirect even if device is set"""
        self.user.staticdevice_set.create(name="default")
        self.strategy.session_set("tfa_completed", True)
        ret = social_pipeline.two_factor_auth(
            self.strategy,
            backend=self.backend,
            details="details",
            pipeline_index=11,
            user=self.user,
            request=self.request,
        )
        self.assertEqual(ret, "details")

    def test_pipeline_with_device(self):
        """Redirect to 2 factor authentication"""
        self.user.staticdevice_set.create(name="default")
        ret = social_pipeline.two_factor_auth(
            self.strategy,
            backend=self.backend,
            details="details",
            pipeline_index=11,
            user=self.user,
            request=self.request,
        )
        self.assertIn("/two-factor-social-auth/", ret.url)
        self.assertTrue(self.strategy.session_get("tfa_partial_token"))

    def test_pipeline_with_device_on_partial_resume(self):
        """Redirect to 2 factor authentication when the pipeline is resumed.

        ``social_core.utils._extend_partial_pipeline`` sets
        ``kwargs["request"]`` to the request *data* when a partial pipeline is
        resumed, so the step cannot read the session off that argument.
        """
        self.user.staticdevice_set.create(name="default")
        ret = social_pipeline.two_factor_auth(
            self.strategy,
            backend=self.backend,
            details="details",
            pipeline_index=11,
            user=self.user,
            request={"code": "code", "state": "state"},
        )
        self.assertIn("/two-factor-social-auth/", ret.url)
        self.assertTrue(self.strategy.session_get("tfa_partial_token"))
