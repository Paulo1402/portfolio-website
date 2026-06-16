import logging
import sys

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db import DatabaseError, connection
from django.db.models import Value
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_POST

from .forms import ContactForm
from .models import Certification, Experience, Formation, Profile, Project, Skill

logger = logging.getLogger(__name__)


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
            "page_title": _("About"),
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

        responsibility_headings = ("Responsabilidades", "Responsibilities")

        for line in experience.description.splitlines():
            if line.startswith(responsibility_headings):
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
        {"page_title": _("Experience"), "experiences": experiences},
    )


def projects(request):
    projects = Project.objects.all().order_by("-start_date")

    # TODO: implement pagination to avoid send many projects with photos to browser

    return render(
        request,
        "pages/projects.html",
        {"page_title": _("Projects"), "projects": projects},
    )


def formation(request):
    formation = Formation.objects.all().order_by("-start_date")

    return render(
        request,
        "pages/formation.html",
        {
            "page_title": _("Education"),
            "formation": formation,
        },
    )


def certifications(request):
    certifications = Certification.objects.all().order_by("-start_date")

    return render(
        request,
        "pages/certifications.html",
        {"page_title": _("Certifications"), "certifications": certifications},
    )


def contact(request):
    profile = Profile.objects.first()

    return render(
        request,
        "pages/contact.html",
        {
            "page_title": _("Contact"),
            "profile": profile,
            "form": ContactForm(),
            "email": profile.email if profile else "",
            "linkedin": {
                "url": profile.linkedin if profile else "",
                "username": profile.linkedin_username if profile else "",
            },
            "github": {
                "url": profile.github if profile else "",
                "username": profile.github_username if profile else "",
            },
        },
    )


@require_POST
def contact_message(request):
    form = ContactForm(request.POST)

    if not form.is_valid():
        messages.error(request, _("Please correct the contact form errors."))
        return redirect("contact")

    profile = Profile.objects.first()
    recipient = settings.CONTACT_EMAIL or (profile.email if profile else "")

    if not recipient:
        messages.error(request, _("Contact email is not configured."))
        return redirect("contact")

    name = form.cleaned_data["name"]
    email = form.cleaned_data["email"]
    message = form.cleaned_data["message"]

    contact_email = EmailMessage(
        subject=_("Portfolio contact from %(name)s") % {"name": name},
        body=_("Name: %(name)s\nEmail: %(email)s\n\n%(message)s")
        % {
            "name": name,
            "email": email,
            "message": message,
        },
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
        reply_to=[email],
    )

    try:
        contact_email.send(fail_silently=False)
    except Exception as e:
        logger.exception("Failed to send contact email", exc_info=e)
        messages.error(
            request, _("Could not send your message. Please try again later.")
        )
        return redirect("contact")

    messages.success(request, _("Message sent successfully!"))

    return redirect("contact")


@require_GET
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError:
        return JsonResponse({"status": "error", "database": "unavailable"}, status=503)

    return JsonResponse({"status": "ok", "database": "available"})


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
