from django.contrib.messages import get_messages
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from app.models import Profile


CONTACT_FORM_DATA = {
    "name": "Ada Lovelace",
    "email": "ada@example.com",
    "message": "Hello from the contact form.",
}


class ContactViewTests(TestCase):
    def test_contact_page_renders_without_profile(self):
        response = self.client.get(reverse("contact"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')

    def test_contact_page_renders_profile_contact_data(self):
        Profile.objects.create(
            description="About me",
            email="paulo@example.com",
            linkedin="https://www.linkedin.com/in/paulo",
            github="https://github.com/paulo1402",
        )

        response = self.client.get(reverse("contact"))

        self.assertContains(response, "paulo@example.com")
        self.assertContains(response, "paulo")
        self.assertContains(response, "paulo1402")

    def test_contact_message_requires_post(self):
        response = self.client.get(reverse("contact_message"))

        self.assertEqual(response.status_code, 405)

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        CONTACT_EMAIL="paulo@example.com",
    )
    def test_invalid_contact_message_does_not_send_email(self):
        response = self.client.post(reverse("contact_message"), data={})

        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="Portfolio Website <noreply@example.com>",
        CONTACT_EMAIL="contact@example.com",
    )
    def test_valid_contact_message_sends_email_to_contact_email(self):
        Profile.objects.create(description="About me", email="profile@example.com")

        response = self.client.post(reverse("contact_message"), data=CONTACT_FORM_DATA)

        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["contact@example.com"])
        self.assertEqual(mail.outbox[0].reply_to, ["ada@example.com"])
        self.assertEqual(
            mail.outbox[0].from_email,
            "Portfolio Website <noreply@example.com>",
        )
        self.assertIn("Ada Lovelace", mail.outbox[0].subject)

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        CONTACT_EMAIL="",
    )
    def test_valid_contact_message_falls_back_to_profile_email(self):
        Profile.objects.create(description="About me", email="profile@example.com")

        response = self.client.post(reverse("contact_message"), data=CONTACT_FORM_DATA)

        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["profile@example.com"])

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        CONTACT_EMAIL="",
    )
    def test_valid_contact_message_without_recipient_shows_error(self):
        response = self.client.post(reverse("contact_message"), data=CONTACT_FORM_DATA)

        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(len(mail.outbox), 0)
        storage = get_messages(response.wsgi_request)

        self.assertIn("Contact email is not configured.", [str(message) for message in storage])
