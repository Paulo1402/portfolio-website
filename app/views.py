import sys

from django.db.models import Value
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Profile, Skill, Experience, Project, Formation, Certification


def index(request):
    profile = Profile.objects.first()
    skills = Skill.objects.filter(show=True, area__show=True).order_by(
        Coalesce(
            "area__index", Value(9999)
        ),  # This field may be null, so it's important to handle before trying to order
        "name",  # Order by skill name
    )

    skills_by_area = {}

    for skill in skills:
        if skill.area not in skills_by_area:
            skills_by_area[skill.area] = []

        skills_by_area[skill.area].append(skill)

    return render(
        request,
        "pages/index.html",
        {
            "page_title": "Sobre mim",
            "profile": profile,
            "skills_by_area": skills_by_area,
        },
    )


def experiences(request):
    experiences = Experience.objects.all().order_by("-start_date")

    # TODO: make this abstraction at the moment we save experiences in admin page
    for experience in experiences:
        responsibility_block = False
        responsibilities = []
        description = []

        for line in experience.description.splitlines():
            if line.startswith("Responsabilidades"):
                responsibility_block = True
            elif responsibility_block:
                line = line.replace("•", "").strip()

                if not line.endswith(";"):
                    line += ";"

                responsibilities.append(line)
            else:
                description.append(line)

        experience.description = "\n".join(description)
        experience.responsibilities = responsibilities

    return render(
        request,
        "pages/experiences.html",
        {"page_title": "Experiências", "experiences": experiences},
    )


def projects(request):
    projects = Project.objects.all().order_by("-start_date")

    # TODO: implement pagination to avoid send many projects with photos to browser

    return render(
        request,
        "pages/projects.html",
        {"page_title": "Projetos", "projects": projects},
    )


def formation(request):
    formation = Formation.objects.all().order_by("-start_date")

    return render(
        request,
        "pages/formation.html",
        {
            "page_title": "Formação",
            "formation": formation,
        },
    )


def certifications(request):
    certifications = Certification.objects.all().order_by("-start_date")

    return render(
        request,
        "pages/certifications.html",
        {"page_title": "Certificações", "certifications": certifications},
    )


def contact(request):
    profile = Profile.objects.first()

    return render(
        request,
        "pages/contact.html",
        {
            "page_title": "Contato",
            "email": profile.email,
            "linkedin": {
                "url": profile.linkedin,
                "username": profile.linkedin_username,
            },
            "github": {
                "url": profile.github,
                "username": profile.github_username,
            },
        },
    )


def contact_message(request):
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    message = request.POST.get("message", "").strip()

    # TODO: handle message sent via contact form
    print(name, email, message)

    messages.success(request, "Mensagem enviada com sucesso!")

    return redirect("contact")


def handler_404(request, *args, **kwargs):
    # TODO: integrate log system
    print("exception 404", args, kwargs)
    return render(request, "global/pages/404.html", status=404)


def handler_500(request, *args, **kwargs):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error_message = str(exc_value)

    # TODO: integrate log system
    print("exception 500", error_message)
    return render(request, "global/pages/500.html", status=500)
