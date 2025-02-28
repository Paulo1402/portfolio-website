from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("experiences/", views.experiences, name="experiences"),
    path("projects/", views.projects, name="projects"),
    path("formation/", views.formation, name="formation"),
    path("certifications/", views.certifications, name="certifications"),
    path("contact/", views.contact, name="contact"),
]
