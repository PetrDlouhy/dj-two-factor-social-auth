from django.test import TestCase
from django.urls import reverse
from model_bakery import baker


class AuthenticationViewTests(TestCase):
    def test_get(self):
        user = baker.make("User")
        baker.make("Partial", token="foo", kwargs={"user": user.id})
        address = reverse("social_2fa:two_factor_authentication") + "?partial_token=foo"
        response = self.client.get(address)
        self.assertContains(
            response,
            '<input type="number" name="otp_token" min="1" max="999999" autofocus="autofocus" '
            'inputmode="numeric" autocomplete="one-time-code" id="id_otp_token">',
            html=True,
        )

    def test_post_invalid_token(self):
        user = baker.make("User")
        baker.make("Partial", token="foo", kwargs={"user": user.id})
        address = reverse("social_2fa:two_factor_authentication") + "?partial_token=foo"
        response = self.client.post(address, {"otp_token": "123456"})
        self.assertContains(
            response,
            "<li>Invalid token. Please make sure you have entered it correctly.</li>",
            html=True,
        )

    def test_post(self):
        user = baker.make("User")
        device = user.staticdevice_set.create()
        device.token_set.create(token="123456")
        partial = baker.make("Partial", token="foo", kwargs={"user": user.id})
        address = reverse("social_2fa:two_factor_authentication") + "?partial_token=foo"
        response = self.client.post(address, {"otp_token": "123456"})
        self.assertRedirects(
            response,
            f"/complete/{partial.backend}/?partial_token=foo",
            fetch_redirect_response=False,
        )
