import tempfile
from PIL import Image

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from airport.models import Crew
from airport.serializers import CrewImageSerializer, CrewSerializer
from airport.views import CrewViewSet


class CrewViewSetTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="password123"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="adminpassword"
        )

        self.crew1 = Crew.objects.create(first_name="John", last_name="Doe")
        self.crew2 = Crew.objects.create(first_name="Jane", last_name="Smith")
        self.crew3 = Crew.objects.create(first_name="Alice", last_name="Brown")
        self.crew4 = Crew.objects.create(first_name="Bob", last_name="Green")

        self.list_url = reverse("airport:crew-list")

    def _get_temporary_image(self):
        """Створює тимчасове тестове зображення."""
        image_file = tempfile.NamedTemporaryFile(suffix=".png")
        Image.new("RGB", (100, 100), color="red").save(image_file)
        image_file.seek(0)
        return image_file

    def _check_paginated_list_response(self, response_data, expected_count):
        self.assertIsInstance(response_data, dict)
        self.assertIn("results", response_data)
        self.assertIsInstance(response_data["results"], list)
        self.assertEqual(response_data["count"], expected_count)
        self.assertEqual(len(response_data["results"]), expected_count)
        if expected_count > 0:
            return response_data["results"][0]
        return None

    def test_list_crews_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_crew_data = self._check_paginated_list_response(response.data, 4)

        self.assertIsNotNone(first_crew_data)
        self.assertIn("John", first_crew_data["first_name"])
        self.assertIn("Doe", first_crew_data["last_name"])
        self.assertIn("image", first_crew_data)

    def test_retrieve_crew_unauthenticated(self):
        url = reverse("airport:crew-detail", args=[self.crew1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.crew1.id)
        self.assertEqual(response.data["first_name"], "John")
        self.assertEqual(response.data["last_name"], "Doe")
        self.assertIn("image", response.data)

    def test_create_crew_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"first_name": "New", "last_name": "CrewMember"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Crew.objects.count(), 5)
        self.assertEqual(response.data["first_name"], "New")
        self.assertEqual(response.data["last_name"], "CrewMember")
        self.assertIsNone(response.data["image"])

    def test_create_crew_as_authenticated_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        data = {"first_name": "Unauthorized", "last_name": "User"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Crew.objects.count(), 4)

    def test_create_crew_unauthenticated_forbidden(self):
        data = {"first_name": "Anon", "last_name": "User"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Crew.objects.count(), 4)

    def test_update_crew_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("airport:crew-detail", args=[self.crew1.id])
        updated_data = {"first_name": "UpdatedJohn", "last_name": "UpdatedDoe"}
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.crew1.refresh_from_db()
        self.assertEqual(self.crew1.first_name, "UpdatedJohn")
        self.assertEqual(self.crew1.last_name, "UpdatedDoe")
        self.assertEqual(response.data["first_name"], "UpdatedJohn")

    def test_partial_update_crew_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("airport:crew-detail", args=[self.crew1.id])
        updated_data = {"first_name": "PartialJohn"}
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.crew1.refresh_from_db()
        self.assertEqual(self.crew1.first_name, "PartialJohn")
        self.assertEqual(self.crew1.last_name, "Doe")
        self.assertEqual(response.data["first_name"], "PartialJohn")

    def test_update_crew_as_authenticated_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("airport:crew-detail", args=[self.crew1.id])
        updated_data = {"first_name": "Forbidden"}
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.crew1.refresh_from_db()
        self.assertEqual(self.crew1.first_name, "John")

    def test_update_crew_unauthenticated_forbidden(self):
        url = reverse("airport:crew-detail", args=[self.crew1.id])
        updated_data = {"first_name": "AnonForbidden"}
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.crew1.refresh_from_db()
        self.assertEqual(self.crew1.first_name, "John")

    def test_delete_crew_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("airport:crew-detail", args=[self.crew1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Crew.objects.count(), 3)
        self.assertFalse(Crew.objects.filter(id=self.crew1.id).exists())

    def test_delete_crew_as_authenticated_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("airport:crew-detail", args=[self.crew1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Crew.objects.count(), 4)

    def test_delete_crew_unauthenticated_forbidden(self):
        url = reverse("airport:crew-detail", args=[self.crew1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Crew.objects.count(), 4)

    def test_upload_image_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("airport:crew-upload-image", args=[self.crew1.id])

        with self._get_temporary_image() as image_file:
            data = {"image": image_file}
            response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.crew1.refresh_from_db()
        self.assertIsNotNone(self.crew1.image)
        self.assertIn("image", response.data)
        self.assertRegex(response.data["image"], r"crew_image_upload/.*\.png")

    def test_upload_image_as_authenticated_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("airport:crew-upload-image", args=[self.crew1.id])

        with self._get_temporary_image() as image_file:
            data = {"image": image_file}
            response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.crew1.refresh_from_db()
        self.assertEqual(self.crew1.image.name, '')

    def test_upload_image_unauthenticated_forbidden(self):
        url = reverse("airport:crew-upload-image", args=[self.crew1.id])

        with self._get_temporary_image() as image_file:
            data = {"image": image_file}
            response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.crew1.refresh_from_db()
        self.assertEqual(self.crew1.image.name, '')

    def test_upload_image_invalid_data(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("airport:crew-upload-image", args=[self.crew1.id])

        with tempfile.NamedTemporaryFile(suffix=".txt") as text_file:
            text_file.write(b"This is not an image.")
            text_file.seek(0)
            data = {"image": text_file}
            response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("image", response.data)

    def test_get_serializer_class_upload_image_action(self):
        factory = RequestFactory()
        request = factory.post(reverse("airport:crew-upload-image", args=[self.crew1.id]))
        request.user = self.admin_user

        view = CrewViewSet()
        view.action = "upload_image"
        view.request = request
        view.kwargs = {"pk": self.crew1.id}
        view.format_kwarg = None

        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, CrewImageSerializer)

    def test_get_serializer_class_list_action(self):
        factory = RequestFactory()
        request = factory.get(self.list_url)
        request.user = self.user

        view = CrewViewSet()
        view.action = "list"
        view.request = request
        view.format_kwarg = None

        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, CrewSerializer)

    def test_get_serializer_class_retrieve_action(self):
        factory = RequestFactory()
        url = reverse("airport:crew-detail", args=[self.crew1.id])
        request = factory.get(url)
        request.user = self.user

        view = CrewViewSet()
        view.action = "retrieve"
        view.request = request
        view.kwargs = {"pk": self.crew1.id}
        view.format_kwarg = None

        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, CrewSerializer)
