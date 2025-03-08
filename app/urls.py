from django.urls import path
import tagulous.views
from .models import Topic

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("experiences/", views.experiences, name="experiences"),
    path("projects/", views.projects, name="projects"),
    path("formation/", views.formation, name="formation"),
    path("certifications/", views.certifications, name="certifications"),
    path("contact/", views.contact, name="contact"),
    path(
        "topic-autocomplete",
        tagulous.views.autocomplete,
        {"tag_model": Topic},
        name="topic_autocomplete",
    ),
]
