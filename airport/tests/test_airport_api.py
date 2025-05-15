from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from airport.models import (
    Crew,
    Order,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Flight,
    Ticket,
)


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            "admin@test.com", "password"
        )
        self.regular_user = get_user_model().objects.create_user(
            "user@test.com", "password"
        )
        self.client.force_authenticate(user=self.regular_user)

        self.airplane_type = AirplaneType.objects.create(name="Airship")
        self.airplane = Airplane.objects.create(
            name="Boeing 747", rows=30, seats_in_row=6, airplane_type=self.airplane_type
        )

        self.route = Route.objects.create(
            source=Airport.objects.create(name="Kyiv", closest_big_city="Kyiv"),
            destination=Airport.objects.create(
                name="Amsterdam", closest_big_city="Amsterdam"
            ),
            distance=30,
        )

        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time="2025-05-16T12:00:00Z",
            arrival_time="2025-05-16T15:00:00Z",
        )

        self.order = Order.objects.create(user=self.regular_user)
        self.ticket = Ticket.objects.create(
            row=2, seat=4, flight=self.flight, order=self.order
        )


class CrewViewSetTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.crew = Crew.objects.create(first_name="Test", last_name="Crew")

    def test_list_crews(self):
        response = self.client.get("/api/crews/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_crew_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            "/api/crews/", {"first_name": "New", "last_name": "Crew"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_upload_image_unauthorized(self):
        response = self.client.post(f"/api/crews/{self.crew.id}/upload-image/", {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrderViewSetTestCase(BaseAPITestCase):
    def test_list_orders_authenticated(self):
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"/api/orders/{self.order.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class FlightViewSetTestCase(BaseAPITestCase):
    def test_list_flights(self):
        response = self.client.get("/api/flights/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_flight_by_destination(self):
        response = self.client.get(f"/api/flights/?destination=Amsterdam")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TicketViewSetTestCase(BaseAPITestCase):
    def test_list_tickets_authenticated(self):
        response = self.client.get("/api/tickets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ticket_authenticated(self):
        response = self.client.post(
            "/api/tickets/",
            {"row": 3, "seat": 2, "flight": self.flight.id, "order": self.order.id},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_ticket_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"/api/tickets/{self.ticket.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
