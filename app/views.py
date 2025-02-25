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

    return render(request, "index.html", {"data": response_json})
