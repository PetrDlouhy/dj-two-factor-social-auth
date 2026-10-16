import random

from django.http import HttpResponseRedirect
from django.test import RequestFactory, TestCase
from model_bakery import baker
from social_core.backends.google import GoogleOAuth2
from social_core.storage import BaseStorage
from social_core.tests.strategy import TestStrategy
from social_django.models import DjangoStorage

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

    def run_step(self, strategy=None, **kwargs):
        return social_pipeline.two_factor_auth(
            strategy or self.strategy,
            backend=self.backend,
            details="details",
            pipeline_index=11,
            user=self.user,
            request=self.request,
            **kwargs,
        )

    def assertChallenged(self, ret):
        self.assertIsInstance(ret, HttpResponseRedirect, "2FA step was skipped")
        self.assertIn("/two-factor-social-auth/", ret.url)

    def test_pipeline_with_device_tfa_completed(self):
        """If the user completed 2FA for the resumed partial, don't redirect even if device is set"""
        self.user.staticdevice_set.create(name="default")
        self.strategy.session_set(
            "tfa_completed", {"user": str(self.user.pk), "partial_token": "foo"}
        )
        self.assertEqual(self.run_step(tfa_partial_token="foo"), "details")

    def test_pipeline_with_device_tfa_completed_is_consumed(self):
        """A completed 2FA step lets one login through, not every later one"""
        self.user.staticdevice_set.create(name="default")
        self.strategy.session_set(
            "tfa_completed", {"user": str(self.user.pk), "partial_token": "foo"}
        )
        self.assertEqual(self.run_step(tfa_partial_token="foo"), "details")
        self.assertIsNone(self.strategy.session_get("tfa_completed"))
        self.assertChallenged(self.run_step(tfa_partial_token="foo"))

    def test_pipeline_with_device_bare_tfa_completed_flag(self):
        """A bare flag, as left in the session by an earlier login, doesn't skip 2FA"""
        self.user.staticdevice_set.create(name="default")
        self.strategy.session_set("tfa_completed", True)
        self.assertChallenged(self.run_step(tfa_partial_token="foo"))

    def test_pipeline_with_device_tfa_completed_by_another_user(self):
        """2FA completed by one account doesn't let a login as another account through"""
        self.user.staticdevice_set.create(name="default")
        other = baker.make("User")
        self.strategy.session_set(
            "tfa_completed", {"user": str(other.pk), "partial_token": "foo"}
        )
        self.assertChallenged(self.run_step(tfa_partial_token="foo"))
        self.assertIsNone(self.strategy.session_get("tfa_completed"))

    def test_pipeline_with_device_tfa_completed_for_another_partial(self):
        """2FA completed for one login attempt doesn't let another attempt through"""
        self.user.staticdevice_set.create(name="default")
        self.strategy.session_set(
            "tfa_completed", {"user": str(self.user.pk), "partial_token": "bar"}
        )
        self.assertChallenged(self.run_step(tfa_partial_token="foo"))

    def test_pipeline_with_device_tfa_completed_on_fresh_login(self):
        """2FA completed for a partial doesn't let a login that resumes no partial through"""
        self.user.staticdevice_set.create(name="default")
        self.strategy.session_set(
            "tfa_completed", {"user": str(self.user.pk), "partial_token": "foo"}
        )
        self.assertChallenged(self.run_step())

    def test_pipeline_resume_of_challenged_partial(self):
        """The resume of the challenged partial is recognised once 2FA is completed for it"""
        self.user.staticdevice_set.create(name="default")
        strategy = TestStrategy(storage=DjangoStorage)
        self.assertChallenged(self.run_step(strategy=strategy))
        token = strategy.session_get("tfa_partial_token")
        resumed = strategy.partial_load(token)
        strategy.session_set(
            "tfa_completed", social_pipeline.tfa_completed_marker(self.user, token)
        )
        ret = social_pipeline.two_factor_auth(
            strategy,
            backend=self.backend,
            pipeline_index=resumed.next_step,
            **resumed.kwargs,
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
