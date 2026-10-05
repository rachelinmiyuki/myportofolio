from main.models import Experience, Project
from main.forms import ProjectForm, ExperienceForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import datetime
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST  
    

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Rachelin Miyuki Hendratmo",
        "npm": "2506536553",
        "study_program": "S1 Information Systems",
        "bio": (
            "IS student at Universitas Indonesia with a strong interest in Product Management and technology-driven problem solving. Passionate about building impactful technology solutions by bridging user needs, business objectives, and technical possibilities."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    title_query = request.GET.get("title", "").strip()
    is_editor = request.user.groups.filter(name="Editor").exists()
    context = {
        "name": "Rachelin Miyuki Hendratmo",
        "title_query": title_query,
        "is_editor": is_editor,
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)
    # json_response = get_experiences_json(request)

    # experiences = serializers.deserialize(
    #     "json",
    #     json_response.content.decode("utf-8"),
    # )
    # experiences = [experience.object for experience in experiences]

    # title_query = request.GET.get("title", "").strip()
    # is_editor = request.user.groups.filter(name="Editor").exists()

    # context = {
    #     "name": "Rachelin Miyuki Hendratmo",
    #     "experience_list": experiences,
    #     "title_query": title_query,
    #     "is_editor": is_editor,
    # }
    # return render(request, "experience.html", context)

# def show_project(request):
#     json_response = get_projects_json(request)

#     projects = serializers.deserialize(
#         "json",
#         json_response.content.decode("utf-8"),
#     )
#     projects = [project.object for project in projects]
#     title_query = request.GET.get("title", "").strip()
#     is_editor = request.user.groups.filter(name="Editor").exists()
#     context = {
#         "name": "Rachelin Miyuki Hendratmo",
#         "project_list": projects,
#         "title_query": title_query,
#         "is_editor": is_editor,
#     }
#     return render(request, "project.html", context)

def show_project(request):
    title_query = request.GET.get("title", "").strip()
    is_editor = request.user.groups.filter(name="Editor").exists()
    context = {
        "name": "Rachelin Miyuki Hendratmo",
        "title_query": title_query,
        "is_editor": is_editor,
        "form": ProjectForm(),
    }
    return render(request, "project.html", context)

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.prefetch_related('starred_by').all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for experience in experiences:
        starred_users = experience.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "category": experience.category,
                "category_display": (experience.get_category_display()),
                "thumbnail": experience.thumbnail,
                "started_at": experience.started_at,
                "ended_at": experience.ended_at,
                "is_ongoing": experience.is_ongoing,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)
    # title_query = request.GET.get("title", "").strip()
    # experiences = Experience.objects.all()

    # if title_query:
    #     experiences = experiences.filter(title__icontains=title_query)

    # experiences_json = serializers.serialize("json", experiences, use_natural_foreign_keys=True)
    # return HttpResponse(experiences_json, content_type="application/json")

# def get_projects_json(request):
#     title_query = request.GET.get("title", "").strip()
#     projects = Project.objects.all();

#     if title_query:
#         projects = projects.filter(title__icontains=title_query)

#     projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
#     return HttpResponse(projects_json, content_type="application/json")

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "project_type": project.project_type,
                "project_type_display": project.get_project_type_display(),
                "thumbnail": project.thumbnail,
                "tag1": project.tag1,
                "tag2": project.tag2,
                "tag3": project.tag3,
                "tag4": project.tag4,
                "detail_url": project.detail_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
            raise PermissionDenied
    
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("main:show_experience")

    context = {
        "name": "Rachelin Miyuki Hendratmo",
        "form": form,
        "is_update": False,
    }
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")  # Tambahkan baris ini
def create_project(request):
    if not request.user.is_superuser:
            raise PermissionDenied
    
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("main:show_project")

    context = {
        "name": "Rachelin Miyuki Hendratmo",
        "form": form,
        "is_update": False,
    }
    return render(request, "projects_form.html", context)

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Proyek berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")

@login_required(login_url="/login/")
def update_experience(request, experience_id):
    is_editor = request.user.groups.filter(name="Editor").exists()
    if not request.user.is_superuser and not is_editor:
            raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)

    form = ExperienceForm(
        request.POST or None,
        instance=experience
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diubah!")
        return redirect("main:show_experience")

    context = {
        "name": "Rachelin Miyuki Hendratmo",
        "form": form,
        "experience": experience,
        "is_update": True,
    }

    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
def update_project(request, project_id):
    is_editor = request.user.groups.filter(name="Editor").exists()
    if not request.user.is_superuser and not is_editor:
                raise PermissionDenied
        
    project = get_object_or_404(Project, pk=project_id)

    form = ProjectForm(
        request.POST or None,
        instance=project
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project berhasil diubah!")
        return redirect("main:show_project")

    context = {
        "name": "Rachelin Miyuki Hendratmo",
        "form": form,
        "project": project,
        "is_update": True,
    }

    return render(request, "projects_form.html", context)

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Rachelin Miyuki Hendratmo",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Rachelin Miyuki Hendratmo",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_project")

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan pengalaman."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Pengalaman berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)