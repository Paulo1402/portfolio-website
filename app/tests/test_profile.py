from django.contrib import admin
from django.core.exceptions import ValidationError
from django.test import RequestFactory, TestCase

from app.admin.profile import ProfileAdmin
from app.models import Profile


class ProfileModelTests(TestCase):
    def test_first_profile_is_valid(self):
        profile = Profile(description="About me")

        profile.full_clean()

    def test_second_profile_is_invalid(self):
        Profile.objects.create(description="Existing profile")
        profile = Profile(description="Second profile")

        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_second_profile_cannot_be_saved_directly(self):
        Profile.objects.create(description="Existing profile")

        with self.assertRaises(ValidationError):
            Profile.objects.create(description="Second profile")


class ProfileAdminTests(TestCase):
    def test_add_permission_is_disabled_when_profile_exists(self):
        Profile.objects.create(description="Existing profile")
        request = RequestFactory().get("/admin/app/profile/add/")
        profile_admin = ProfileAdmin(Profile, admin.site)

        self.assertFalse(profile_admin.has_add_permission(request))
