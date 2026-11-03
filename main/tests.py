from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User, Group
from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

        self.project = Project.objects.create(
            title="FisioMate",
            description="AI-powered physiotherapy platform connecting patients and physiotherapists.",
            project_type="competition",
            thumbnail="https://res.cloudinary.com/jer1ev6h/image/upload/v1789370884/DSC01844.jpg",
            tag1="Product Management",
            tag2="User Research",
            tag3="Business Strategy",
            tag4="AI",
            detail_url="https://drive.google.com/file/d/1L-llvyIjN4tuIUEVH4-OP9lrDNhhL518/view?usp=sharing",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')
        self.assertNotContains(response, self.project.title)
        self.assertContains(response, f'href="{reverse("main:show_project")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)


    #tes untuk experience
    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(
            response,
            f'href="{reverse("main:show_main")}"'
        )

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()

        self.assertFalse(self.experience.is_ongoing)

    # tes untuk projects
    def test_project_model(self):
        self.assertEqual(str(self.project), "FisioMate")
        self.assertEqual(self.project.project_type, "competition")
        self.assertEqual(self.project.tag1, "Product Management")
        self.assertEqual(self.project.tag2, "User Research")
        self.assertEqual(self.project.tag3, "Business Strategy")
        self.assertEqual(self.project.tag4, "AI")

    def test_project_page(self):
        response = self.client.get(reverse("main:show_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project.html")
        self.assertContains(
            response,
            'id="project-swiper"'
        )
        self.assertContains(
            response,
            'id="project-swiper-wrapper"'
        )
        self.assertContains(
            response,
            'id="project-search-form"'
        )
        self.assertContains(
            response,
            f'href="{reverse("main:show_main")}"'
        )

    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_project"))

        self.assertContains(response, "Belum ada project yang ditambahkan.")

    def test_editor_can_patch_project(self):
        editor = User.objects.create_user(
            username="editor",
            password="testpassword123",
        )
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        editor.groups.add(editor_group)

        self.client.force_login(editor)

        response = self.client.patch(
            reverse("api:project-detail", args=[self.project.id]),
            {"title": "Updated by Editor"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Updated by Editor")


    def test_editor_cannot_create_project(self):
        editor = User.objects.create_user(
            username="editor",
            password="testpassword123",
        )
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        editor.groups.add(editor_group)

        self.client.force_login(editor)

        response = self.client.post(
            reverse("api:project-list"),
            {
                "title": "New Project",
                "description": "Project description",
                "project_type": "competition",
                "thumbnail": "https://example.com/image.jpg",
                "tag1": "Django",
                "detail_url": "https://example.com",
            },
        )

        self.assertEqual(response.status_code, 403)


    def test_editor_cannot_delete_project(self):
        editor = User.objects.create_user(
            username="editor",
            password="testpassword123",
        )
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        editor.groups.add(editor_group)

        self.client.force_login(editor)

        response = self.client.delete(
            reverse("api:project-detail", args=[self.project.id])
        )

        self.assertEqual(response.status_code, 403) 