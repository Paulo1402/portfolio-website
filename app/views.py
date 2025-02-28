from django.conf import settings
from django.shortcuts import render
import requests

# Create your views here.


def index(request):
    # response = requests.get(
    #     "https://api.github.com/user",
    #     headers={"Authorization": f"Bearer {settings.GITHUB_TOKEN}"},
    # )
    # response_json = response.json()

    return render(
        request,
        "pages/index.html",
        {
            "page_title": "Sobre mim",
        },
    )


def experiences(request):
    return render(request, "pages/experiences.html", {"page_title": "Experiências"})


def projects(request):
    return render(request, "pages/projects.html", {"page_title": "Projetos"})


def formation(request):
    return render(request, "pages/formation.html", {"page_title": "Formação"})


def certifications(request):
    return render(request, "pages/certifications.html", {"page_title": "Certificações"})


def contact(request):
    return render(
        request,
        "pages/contact.html",
        {
            "page_title": "Contato",
            "email": settings.EMAIL,
            "linkedin": {
                "url": settings.LINKEDIN,
                "username": settings.LINKEDIN.split("/")[-2],
            },
        },
    )


def handler_404(request, exception):
    print("exception", exception)
    return render(request, "global/pages/404.html", status=404)
