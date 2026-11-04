from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    def test_home_page_renders_without_profile(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Zen of Python")

    def test_home_page_uses_language_url_prefix(self):
        response = self.client.get("/pt-br/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.LANGUAGE_CODE, "pt-br")
        self.assertContains(response, "Sobre mim")
        self.assertNotContains(response, ">About<", html=False)

        response = self.client.get("/en/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.LANGUAGE_CODE, "en")
        self.assertContains(response, ">About<", html=False)
