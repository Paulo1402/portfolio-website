from django.conf import settings
from django.shortcuts import render
import requests

# Create your views here.


def index(request):
    response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {settings.GITHUB_TOKEN}"},
    )
    response_json = response.json()

    return render(request, "pages/index.html", {"data": response_json})


def about(request):
    return render(request, "pages/about.html")


def contact(request):
    return render(request, "pages/contact.html")


def handler_404(request, exception):
    print("exception", exception)
    return render(request, "global/pages/404.html", status=404)
