from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from airport.models import (
    Order,
    Ticket,
    Flight,
    Airplane,
    AirplaneType,
    Route,
    Airport,
)
from airport.serializers import OrderSerializer, OrderListSerializer
from airport.views import OrderViewSet


class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="password123"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="adminpassword"
        )

        self.airplane_type = AirplaneType.objects.create(name="Boeing")
        self.airplane = Airplane.objects.create(
            name="Test Plane", rows=10, seats_in_row=6, airplane_type=self.airplane_type
        )
        self.airport_source = Airport.objects.create(
            name="Test Airport Source", closest_big_city="City A"
        )
        self.airport_destination = Airport.objects.create(
            name="Test Airport Dest", closest_big_city="City B"
        )
        self.route = Route.objects.create(
            source=self.airport_source, destination=self.airport_destination, distance=1000
        )

        self.flight1 = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now() + timedelta(days=1),
            arrival_time=timezone.now() + timedelta(days=1, hours=3),
        )
        self.flight2 = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now() + timedelta(days=2),
            arrival_time=timezone.now() + timedelta(days=2, hours=3),
        )

        self.order1_user = Order.objects.create(user=self.user)
        Ticket.objects.create(order=self.order1_user, flight=self.flight1, row=1, seat=1)
        Ticket.objects.create(order=self.order1_user, flight=self.flight1, row=1, seat=2)

        self.order2_admin = Order.objects.create(user=self.admin_user)
        Ticket.objects.create(order=self.order2_admin, flight=self.flight2, row=2, seat=1)

        self.list_url = reverse("airport:order-list")

    def _check_paginated_list_response(self, response_data, expected_count):
        self.assertIsInstance(response_data, dict)
        self.assertIn("results", response_data)
        self.assertIsInstance(response_data["results"], list)
        self.assertEqual(response_data["count"], expected_count)
        self.assertEqual(len(response_data["results"]), expected_count)
        if expected_count > 0:
            return response_data["results"][0]
        return None

    def test_list_orders_authenticated_user_only_own_orders(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_order_data = self._check_paginated_list_response(response.data, 1)

        self.assertEqual(first_order_data["id"], self.order1_user.id)
        self.assertIn("tickets", first_order_data)
        self.assertIsInstance(first_order_data["tickets"], list)
        self.assertEqual(len(first_order_data["tickets"]), 2)
        self.assertIn("row", first_order_data["tickets"][0])

    def test_list_orders_admin_sees_all_orders(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Очікуємо 2 замовлення (одне користувача, одне адміна)
        first_order_data = self._check_paginated_list_response(response.data, 2)

        order_ids = [order["id"] for order in response.data["results"]]
        self.assertIn(self.order1_user.id, order_ids)
        self.assertIn(self.order2_admin.id, order_ids)

    def test_list_orders_unauthenticated_forbidden(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_order_authenticated_user_own_order(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("airport:order-detail", args=[self.order1_user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.order1_user.id)
        self.assertIn("tickets", response.data)
        self.assertEqual(len(response.data["tickets"]), 2)

    def test_retrieve_order_authenticated_user_other_user_order_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("airport:order-detail", args=[self.order2_admin.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # Або 403, залежить від вашої політики

    def test_retrieve_order_admin_any_order(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("airport:order-detail", args=[self.order1_user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.order1_user.id)
        self.assertIn("tickets", response.data)

    def test_retrieve_order_unauthenticated_forbidden(self):
        url = reverse("airport:order-detail", args=[self.order1_user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "tickets": [
                {"flight": self.flight1.id, "row": 5, "seat": 3},
                {"flight": self.flight2.id, "row": 6, "seat": 1},
            ]
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 3)
        self.assertEqual(Ticket.objects.count(), 5)

        new_order = Order.objects.get(id=response.data["id"])
        self.assertEqual(new_order.user, self.user)
        self.assertEqual(new_order.tickets.count(), 2)

        self.assertIn("tickets", response.data)
        self.assertEqual(len(response.data["tickets"]), 2)
        self.assertIn("id", response.data["tickets"][0])
        self.assertIn("row", response.data["tickets"][0])
        self.assertIn("seat", response.data["tickets"][0])
        self.assertIn("flight", response.data["tickets"][0])

    def test_create_order_authenticated_user_empty_tickets(self):
        self.client.force_authenticate(user=self.user)
        data = {"tickets": []}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 3)
        self.assertEqual(Ticket.objects.count(), 3)

        new_order = Order.objects.get(id=response.data["id"])
        self.assertEqual(new_order.user, self.user)
        self.assertEqual(new_order.tickets.count(), 0)

    def test_create_order_authenticated_user_invalid_ticket_data(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "tickets": [
                {"flight": self.flight1.id, "row": 1, "seat": 1},
                {"flight": self.flight2.id, "row": 7, "seat": 700},
            ]
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("tickets", response.data)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Ticket.objects.count(), 3)

    def test_create_order_unauthenticated_forbidden(self):
        data = {
            "tickets": [
                {"flight": self.flight1.id, "row": 5, "seat": 3}
            ]
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Order.objects.count(), 2)

    def test_update_order_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("airport:order-detail", args=[self.order1_user.id])
        updated_data = {"created_at": timezone.now().isoformat()}
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_order_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("airport:order-detail", args=[self.order1_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Order.objects.count(), 2)

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Order.objects.count(), 2)

    def test_get_serializer_class_list_action(self):
        factory = RequestFactory()
        request = factory.get(self.list_url)
        request.user = self.user

        view = OrderViewSet()
        view.action = "list"
        view.request = request
        view.format_kwarg = None

        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, OrderListSerializer)

    def test_get_serializer_class_retrieve_create_actions(self):
        factory = RequestFactory()

        retrieve_url = reverse("airport:order-detail", args=[self.order1_user.id])
        request_retrieve = factory.get(retrieve_url)
        request_retrieve.user = self.user

        view_retrieve = OrderViewSet()
        view_retrieve.action = "retrieve"
        view_retrieve.request = request_retrieve
        view_retrieve.kwargs = {"pk": self.order1_user.id}
        view_retrieve.format_kwarg = None

        serializer_class_retrieve = view_retrieve.get_serializer_class()
        self.assertEqual(serializer_class_retrieve, OrderSerializer)

        request_create = factory.post(self.list_url)
        request_create.user = self.user

        view_create = OrderViewSet()
        view_create.action = "create"
        view_create.request = request_create
        view_create.format_kwarg = None

        serializer_class_create = view_create.get_serializer_class()
        self.assertEqual(serializer_class_create, OrderSerializer)
