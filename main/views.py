from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Rachelin Miyuki Hendratmo",
        "npm": "2506536553",
        "study_program": "S1 Information Systems",
        "bio": (
            "IS student at Universitas Indonesia with a strong interest in Product Management and technology-driven problem solving. Passionate about building impactful technology solutions by bridging user needs, business objectives, and technical possibilities."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Rachelin Miyuki Hendratmo",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)