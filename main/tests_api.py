
import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.utils.html import strip_tags
from rest_framework import serializers
from main.models import Project, Experience


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner",
            password="test-password",
            email="owner@example.com",
        )

        self.visitor = User.objects.create_user(
            username="visitor",
            password="test-password",
        )

        self.project = Project.objects.create(
            title="Portfolio",
            description="My website",
            project_type="website",
            thumbnail="https://example.com/image.png",
            tag1="Django",
            tag2="Python",
            tag3="HTML",
            tag4="CSS",
            detail_url="https://example.com/",
        )

        self.list_url = reverse("api:project-list")
        self.detail_url = reverse(
            "api:project-detail",
            args=[self.project.id],
        )
        self.star_url = reverse(
            "api:project-star",
            args=[self.project.id],
        )

        self.payload = {
            "title": "New project",
            "description": "A useful app",
            "project_type": "website",
            "thumbnail": "https://example.com/new-image.png",
            "tag1": "Django",
            "tag2": "Python",
            "tag3": "HTML",
            "tag4": "CSS",
            "detail_url": "https://example.com/new-project/",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data[0]["id"],
            str(self.project.id),
        )
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])

        self.assertEqual(
            self.client.get(self.detail_url).status_code,
            status.HTTP_200_OK,
        )

    def test_search_and_empty_results(self):
        response = self.client.get(
            self.list_url,
            {"title": "PORT"},
        )
        self.assertEqual(len(response.data), 1)

        response = self.client.get(
            self.list_url,
            {"title": "not-found"},
        )
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse(
            "api:project-detail",
            args=[uuid.uuid4()],
        )

        self.assertEqual(
            self.client.get(url).status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)

            self.assertEqual(
                self.client.post(
                    self.list_url,
                    self.payload,
                    format="json",
                ).status_code,
                status.HTTP_403_FORBIDDEN,
            )

            self.assertEqual(
                self.client.patch(
                    self.detail_url,
                    {"title": "Changed"},
                    format="json",
                ).status_code,
                status.HTTP_403_FORBIDDEN,
            )

            self.assertEqual(
                self.client.delete(self.detail_url).status_code,
                status.HTTP_403_FORBIDDEN,
            )

        self.assertEqual(Project.objects.count(), 1)

        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Project.objects.filter(pk=response.data["id"]).exists()
        )

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)

        for changes, field in [
            ({"title": "   "}, "title"),
            (
                {"title": '<img src="x" onerror="alert(1)">'},
                "title",
            ),
            (
                {"detail_url": "javascript:alert(1)"},
                "detail_url",
            ),
        ]:
            response = self.client.post(
                self.list_url,
                {**self.payload, **changes},
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )
            self.assertIn(field, response.data)

        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.detail_url,
            {"title": "Changed"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Changed")
        self.assertEqual(self.project.description, "My website")

        response = self.client.put(
            self.detail_url,
            {"title": "Incomplete"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(response.content, b"")

        self.assertFalse(
            Project.objects.filter(pk=self.project.id).exists()
        )

    def test_star_requires_login_and_toggles(self):
        response = self.client.post(self.star_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.client.force_authenticate(user=self.visitor)

        response = self.client.post(self.star_url)

        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

        response = self.client.post(self.star_url)

        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            {
                **self.payload,
                "star_count": 99,
                "is_starred": True,
                "starred_by_names": "forged",
                "starred_by": [self.visitor.id],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    
    def test_staff_cannot_manage_tutorial_projects(self):
        staff = User.objects.create_user(
            username="staff",
            password="testpassword123",
            is_staff=True,
        )

        self.client.force_login(staff)

        response = self.client.patch(
            reverse("api:project-detail", args=[self.project.id]),
            {"title": "Updated by Staff"},
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)

        self.assertEqual(
            self.client.delete(self.list_url).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)

        self.assertTrue(
            client.login(
                username="owner",
                password="test-password",
            )
        )

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)

        client.login(
            username="owner",
            password="test-password",
        )

        page = client.get(
            self.list_url,
            HTTP_ACCEPT="text/html",
        )

        self.assertEqual(
            page.status_code,
            status.HTTP_200_OK,
        )

        token = client.cookies["csrftoken"].value

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="experience_owner",
            password="test-password",
            email="experience_owner@example.com",
        )

        self.visitor = User.objects.create_user(
            username="experience_visitor",
            password="test-password",
        )

        self.editor_group = Group.objects.create(name="Editor")
        self.editor = User.objects.create_user(
            username="experience_editor",
            password="test-password",
        )
        self.editor.groups.add(self.editor_group)

        self.experience = Experience.objects.create(
            title="Staff Open House",
            description="Bertugas sebagai staff.",
            category="organization",
            thumbnail="https://example.com/experience.png",
        )

        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse(
            "api:experience-detail",
            args=[self.experience.id],
        )
        self.star_url = reverse(
            "api:experience-star",
            args=[self.experience.id],
        )

        self.payload = {
            "title": "Project Manager",
            "description": "Mengelola jalannya proyek.",
            "category": "committee",
            "thumbnail": "https://example.com/new-experience.png",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["id"],
            str(self.experience.id),
        )
        self.assertEqual(
            response.data[0]["category_display"],
            self.experience.get_category_display(),
        )
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(
            self.list_url,
            {"title": "OPEN"},
        )
        self.assertEqual(len(response.data), 1)

        response = self.client.get(
            self.list_url,
            {"title": "not-found"},
        )
        self.assertEqual(response.data, [])

    def test_missing_experience(self):
        url = reverse(
            "api:experience-detail",
            args=[uuid.uuid4()],
        )
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)

            response = self.client.post(
                self.list_url,
                self.payload,
                format="json",
            )
            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            response = self.client.patch(
                self.detail_url,
                {"title": "Changed"},
                format="json",
            )
            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            response = self.client.delete(self.detail_url)
            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Staff Open House")

    def test_editor_can_patch_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.patch(
            self.detail_url,
            {"title": "Updated by Editor"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.experience.refresh_from_db()
        self.assertEqual(
            self.experience.title,
            "Updated by Editor",
        )

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        response = self.client.delete(self.detail_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(Experience.objects.count(), 1)

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(
            Experience.objects.filter(pk=response.data["id"]).exists()
        )

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(self.detail_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Experience.objects.filter(pk=self.experience.id).exists()
        )

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)

        invalid_payloads = [
            {"title": "   "},
            {"title": "<script>alert(1)</script>"},
            {"category": "invalid-category"},
        ]

        for changes in invalid_payloads:
            response = self.client.post(
                self.list_url,
                {**self.payload, **changes},
                format="json",
            )
            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
                msg=f"Payload gagal: {changes}, response: {response.data}",
            )

        self.assertEqual(Experience.objects.count(), 1)

    def test_star_requires_login_and_toggles(self):
        response = self.client.post(self.star_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.client.force_authenticate(user=self.visitor)

        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            {
                **self.payload,
                "star_count": 99,
                "is_starred": True,
                "starred_by_names": "forged",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_csrf_protection(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        csrf_client.login(
            username="experience_owner",
            password="test-password",
        )

        response = csrf_client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )