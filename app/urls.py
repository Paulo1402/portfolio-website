import tagulous.views
from django.urls import path

from . import views
from .models import Topic

# app_name = "portfolio"

urlpatterns = [
    path("", views.index, name="home"),
    path("experiences/", views.experiences, name="experiences"),
    path("projects/", views.projects, name="projects"),
    path("formation/", views.formation, name="formation"),
    path("certifications/", views.certifications, name="certifications"),
    path("contact/", views.contact, name="contact"),
    path("contact/message", views.contact_message, name="contact_message"),
    path(
        "topic-autocomplete",
        tagulous.views.autocomplete,
        {"tag_model": Topic},
        name="topic_autocomplete",
    ),
]
