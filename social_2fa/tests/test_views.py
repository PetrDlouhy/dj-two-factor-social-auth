from django.test import TestCase
from django.urls import reverse
from model_bakery import baker


class AuthenticationViewTests(TestCase):
    def setUp(self):
        self.user = baker.make("User")
        session = self.client.session
        session["tfa_social_user_id"] = self.user.id
        session["tfa_social_backend"] = "test-backend"
        session.save()
        self.address = reverse("social_2fa:two_factor_authentication")

    def test_get(self):
        response = self.client.get(self.address)
        self.assertContains(
            response,
            '<input type="text" name="otp_token" maxlength="6" minlength="6" autofocus="autofocus"'
            'pattern="[0-9]*" autocomplete="one-time-code" id="id_otp_token">',
            html=True,
        )

    def test_post_invalid_token(self):
        response = self.client.post(self.address, {"otp_token": "123456"})
        self.assertContains(
            response,
            "<li>Invalid token. Please make sure you have entered it correctly.</li>",
            html=True,
        )

    def test_post(self):
        device = self.user.staticdevice_set.create()
        device.token_set.create(token="123456")
        response = self.client.post(self.address, {"otp_token": "123456"})
        self.assertRedirects(
            response,
            "/complete/test-backend/",
            fetch_redirect_response=False,
        )
