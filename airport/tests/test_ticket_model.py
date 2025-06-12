from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from airport.models import Ticket, Flight, Order, Airplane, AirplaneType, Airport, Route


class TicketModelTest(TestCase):

    def setUp(self):
        self.airplane_type_jet = AirplaneType.objects.create(name="Jet")

        self.airplane_small = Airplane.objects.create(
            name="Small Plane",
            rows=10,
            seats_in_row=4,
            airplane_type=self.airplane_type_jet
        )
        self.airplane_large = Airplane.objects.create(
            name="Large Plane",
            rows=20,
            seats_in_row=6,
            airplane_type=self.airplane_type_jet
        )

        self.airport_source = Airport.objects.create(name="Airport A", closest_big_city="City A")
        self.airport_destination = Airport.objects.create(name="Airport B", closest_big_city="City B")

        self.route1 = Route.objects.create(
            source=self.airport_source,
            destination=self.airport_destination,
            distance=1000
        )

        self.flight_small = Flight.objects.create(
            airplane=self.airplane_small,
            route=self.route1,
            departure_time=timezone.now() + timedelta(days=1, hours=10),
            arrival_time=timezone.now() + timedelta(days=1, hours=12),
        )
        self.flight_large = Flight.objects.create(
            airplane=self.airplane_large,
            route=self.route1,
            departure_time=timezone.now() + timedelta(days=2, hours=14),
            arrival_time=timezone.now() + timedelta(days=2, hours=17),
        )

        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="password123"
        )
        self.order1 = Order.objects.create(user=self.user, created_at=timezone.now())
        self.order2 = Order.objects.create(user=self.user, created_at=timezone.now())

    def test_save_valid_ticket(self):
        ticket = Ticket(
            row=1,
            seat=1,
            flight=self.flight_small,
            order=self.order1
        )
        ticket.save()
        self.assertIsNotNone(ticket.id)

        retrieved_ticket = Ticket.objects.get(id=ticket.id)
        self.assertEqual(retrieved_ticket.row, 1)
        self.assertEqual(retrieved_ticket.seat, 1)
        self.assertEqual(retrieved_ticket.flight, self.flight_small)
        self.assertEqual(retrieved_ticket.order, self.order1)

    def test_str_representation(self):
        ticket = Ticket(
            row=7,
            seat=2,
            flight=self.flight_large,
            order=self.order1
        )
        expected_str = f"{self.flight_large}: (row: 7, seat: 2)"
        self.assertEqual(str(ticket), expected_str)
