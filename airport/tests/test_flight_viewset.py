from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone

from airport.models import (
    Flight,
    Airplane,
    AirplaneType,
    Route,
    Airport,
    Order,
    Ticket,
    Crew,
)


class FlightViewSetTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="password123"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="adminpassword"
        )

        self.airplane_type_jet = AirplaneType.objects.create(name="Jet")
        self.airplane_type_prop = AirplaneType.objects.create(name="Propeller")

        self.airplane_small = Airplane.objects.create(
            name="Boeing 737", rows=10, seats_in_row=6, airplane_type=self.airplane_type_jet
        )
        self.airplane_large = Airplane.objects.create(
            name="Airbus A380", rows=20, seats_in_row=10, airplane_type=self.airplane_type_jet
        )

        self.airport_london = Airport.objects.create(
            name="Heathrow Airport", closest_big_city="London"
        )
        self.airport_paris = Airport.objects.create(
            name="Charles de Gaulle Airport", closest_big_city="Paris"
        )
        self.airport_berlin = Airport.objects.create(
            name="Berlin Brandenburg Airport", closest_big_city="Berlin"
        )
        self.airport_dublin = Airport.objects.create(
            name="Dublin Airport", closest_big_city="Dublin"
        )

        self.route_london_paris = Route.objects.create(
            source=self.airport_london, destination=self.airport_paris, distance=500
        )
        self.route_paris_berlin = Route.objects.create(
            source=self.airport_paris, destination=self.airport_berlin, distance=700
        )
        self.route_london_berlin = Route.objects.create(
            source=self.airport_london, destination=self.airport_berlin, distance=1000
        )
        self.route_paris_dublin = Route.objects.create(
            source=self.airport_paris, destination=self.airport_dublin, distance=800
        )

        self.crew1 = Crew.objects.create(first_name="John", last_name="Doe")
        self.crew2 = Crew.objects.create(first_name="Jane", last_name="Smith")

        self.flight1 = Flight.objects.create(
            route=self.route_london_paris,
            airplane=self.airplane_small,
            departure_time=timezone.now() + timedelta(days=1, hours=10),
            arrival_time=timezone.now() + timedelta(days=1, hours=12),
        )
        self.flight1.crews.add(self.crew1)

        self.flight2 = Flight.objects.create(
            route=self.route_paris_berlin,
            airplane=self.airplane_large,
            departure_time=timezone.now() + timedelta(days=2, hours=14),
            arrival_time=timezone.now() + timedelta(days=2, hours=17),
        )
        self.flight2.crews.add(self.crew2)

        self.flight3 = Flight.objects.create(
            route=self.route_london_berlin,
            airplane=self.airplane_small,
            departure_time=timezone.now() + timedelta(days=3, hours=8),
            arrival_time=timezone.now() + timedelta(days=3, hours=11),
        )
        self.flight3.crews.add(self.crew1, self.crew2)

        self.flight4 = Flight.objects.create(
            route=self.route_paris_dublin,
            airplane=self.airplane_large,
            departure_time=timezone.now() + timedelta(days=4, hours=9),
            arrival_time=timezone.now() + timedelta(days=4, hours=12),
        )
        self.flight4.crews.add(self.crew2)

        self.order1 = Order.objects.create(user=self.user, created_at=timezone.now())
        Ticket.objects.create(row=1, seat=1, flight=self.flight1, order=self.order1)
        Ticket.objects.create(row=1, seat=2, flight=self.flight1, order=self.order1)

        self.flight1_total_capacity = (
                self.flight1.airplane.rows * self.flight1.airplane.seats_in_row
        )
        self.flight1_available_tickets = self.flight1_total_capacity - 2

    def _check_list_response(self, response_data, expected_count):
        self.assertIsInstance(response_data, dict)
        self.assertIn("results", response_data)
        self.assertIsInstance(response_data["results"], list)
        self.assertEqual(response_data["count"], expected_count)
        self.assertEqual(len(response_data["results"]), expected_count)
        if expected_count > 0:
            return response_data["results"][0]
        return None


    def test_list_flights_unauthenticated(self):
        url = reverse("airport:flight-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_flight_data = self._check_list_response(response.data, 4)

        self.assertIsNotNone(first_flight_data)

        self.assertIn("tickets_available", first_flight_data)
        found_flight1_data = next((f for f in response.data["results"] if f["id"] == self.flight1.id), None)
        self.assertIsNotNone(found_flight1_data)
        self.assertEqual(found_flight1_data["tickets_available"], self.flight1_available_tickets)

        self.assertIn("route", first_flight_data)
        self.assertIn("source", first_flight_data["route"])
        self.assertIn("destination", first_flight_data["route"])

        self.assertIn("airplane", first_flight_data)
        self.assertIsInstance(first_flight_data["airplane"], str)

        self.assertNotIn("crews", first_flight_data)
        self.assertNotIn("tickets", first_flight_data)
        self.assertNotIn("taken_places", first_flight_data)

    def test_retrieve_flight_unauthenticated(self):
        url = reverse("airport:flight-detail", args=[self.flight1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.flight1.id)

        self.assertIn("crews", response.data)
        self.assertIsInstance(response.data["crews"], list)
        self.assertGreater(len(response.data["crews"]), 0)
        self.assertIn("first_name", response.data["crews"][0])

        self.assertIn("taken_places", response.data)
        self.assertIsInstance(response.data["taken_places"], list)
        self.assertGreater(len(response.data["taken_places"]), 0)
        self.assertIn("row", response.data["taken_places"][0])

        self.assertNotIn("tickets_available", response.data)

        self.assertIn("route", response.data)
        self.assertIn("name", response.data["route"]["source"])
        self.assertIn("distance", response.data["route"])
        self.assertIn("airplane", response.data)
        self.assertIn("rows", response.data["airplane"])

    def test_list_flights_filter_by_route(self):
        url = reverse("airport:flight-list")
        response = self.client.get(url, {"route": self.route_london_paris.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_flight_data = self._check_list_response(response.data, 1)
        self.assertEqual(first_flight_data["id"], self.flight1.id)

    def test_list_flights_filter_by_source(self):
        url = reverse("airport:flight-list")
        response = self.client.get(url, {"source": "london"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data_results = self._check_list_response(response.data, 2)
        self.assertIsNotNone(response_data_results)
        flight_ids = [f["id"] for f in response.data["results"]]
        self.assertIn(self.flight1.id, flight_ids)
        self.assertIn(self.flight3.id, flight_ids)

    def test_list_flights_filter_by_destination(self):
        url = reverse("airport:flight-list")
        response = self.client.get(url, {"destination": "berlin"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data_results = self._check_list_response(response.data, 2)
        self.assertIsNotNone(response_data_results)
        flight_ids = [f["id"] for f in response.data["results"]]
        self.assertIn(self.flight2.id, flight_ids)
        self.assertIn(self.flight3.id, flight_ids)

    def test_list_flights_filter_multiple_params(self):
        url = reverse("airport:flight-list")
        response = self.client.get(url, {"source": "london", "destination": "berlin"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data_results = self._check_list_response(response.data, 1)
        self.assertIsNotNone(response_data_results)
        self.assertEqual(response_data_results["id"], self.flight3.id)

    def test_create_flight_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("airport:flight-list")
        data = {
            "route": self.route_london_paris.id,
            "airplane": self.airplane_small.id,
            "departure_time": (timezone.now() + timedelta(days=5, hours=10)).isoformat(),
            "arrival_time": (timezone.now() + timedelta(days=5, hours=12)).isoformat(),
            "crews": [self.crew1.id, self.crew2.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flight.objects.count(), 5)

        new_flight = Flight.objects.get(id=response.data["id"])
        self.assertEqual(response.data["route"], self.route_london_paris.id)
        self.assertEqual(response.data["airplane"], self.airplane_small.id)
        self.assertNotIn("crews", response.data)

        self.assertCountEqual(
            [crew.id for crew in new_flight.crews.all()],
            []
        )

    def test_create_flight_as_authenticated_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("airport:flight-list")
        data = {
            "route": self.route_london_paris.id,
            "airplane": self.airplane_small.id,
            "departure_time": (timezone.now() + timedelta(days=5, hours=10)).isoformat(),
            "arrival_time": (timezone.now() + timedelta(days=5, hours=12)).isoformat(),
            "crews": []
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Flight.objects.count(), 4)

    def test_create_flight_unauthenticated_forbidden(self):
        url = reverse("airport:flight-list")
        data = {
            "route": self.route_london_paris.id,
            "airplane": self.airplane_small.id,
            "departure_time": (timezone.now() + timedelta(days=5, hours=10)).isoformat(),
            "arrival_time": (timezone.now() + timedelta(days=5, hours=12)).isoformat(),
            "crews": []
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Flight.objects.count(), 4)


    def test_update_flight_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("airport:flight-detail", args=[self.flight1.id])
        updated_data = {
            "route": self.route_paris_berlin.id,
            "airplane": self.airplane_large.id,
            "departure_time": (timezone.now() + timedelta(days=10, hours=9)).isoformat(),
            "arrival_time": (timezone.now() + timedelta(days=10, hours=11)).isoformat(),
            "crews": [self.crew2.id]
        }
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.flight1.refresh_from_db()

        self.assertEqual(self.flight1.route, self.route_paris_berlin)
        self.assertEqual(self.flight1.airplane, self.airplane_large)
        self.assertNotIn("crews", response.data)

        self.assertCountEqual(
            [crew.id for crew in self.flight1.crews.all()],
            [self.crew1.id]
        )

    def test_partial_update_flight_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("airport:flight-detail", args=[self.flight1.id])
        updated_data = {
            "departure_time": (timezone.now() + timedelta(days=15, hours=8)).isoformat(),
        }
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.flight1.refresh_from_db()
        self.assertAlmostEqual(
            self.flight1.departure_time,
            timezone.datetime.fromisoformat(updated_data["departure_time"]),
            delta=timedelta(seconds=1)
        )
        self.assertEqual(self.flight1.route, self.route_london_paris)

    def test_update_flight_as_authenticated_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("airport:flight-detail", args=[self.flight1.id])
        updated_data = {
            "route": self.route_paris_berlin.id,
        }
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.flight1.refresh_from_db()
        self.assertEqual(self.flight1.route, self.route_london_paris)

    def test_update_flight_unauthenticated_forbidden(self):
        url = reverse("airport:flight-detail", args=[self.flight1.id])
        updated_data = {
            "route": self.route_paris_berlin.id,
        }
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.flight1.refresh_from_db()
        self.assertEqual(self.flight1.route, self.route_london_paris)

    def test_delete_flight_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("airport:flight-detail", args=[self.flight1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Flight.objects.count(), 3)
        self.assertFalse(Flight.objects.filter(id=self.flight1.id).exists())

    def test_delete_flight_as_authenticated_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("airport:flight-detail", args=[self.flight1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Flight.objects.count(), 4)

    def test_delete_flight_unauthenticated_forbidden(self):
        url = reverse("airport:flight-detail", args=[self.flight1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Flight.objects.count(), 4)

    def test_get_serializer_class_list_action(self):
        url = reverse("airport:flight-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_flight_data = self._check_list_response(response.data, 4)

        self.assertIsNotNone(first_flight_data)

        self.assertIn("tickets_available", first_flight_data)
        self.assertIsInstance(first_flight_data["tickets_available"], int)

        self.assertIn("route", first_flight_data)
        self.assertIn("source", first_flight_data["route"])
        self.assertIn("destination", first_flight_data["route"])
        self.assertIn("airplane", first_flight_data)
        self.assertIsInstance(first_flight_data["airplane"], str)

        self.assertNotIn("crews", first_flight_data)
        self.assertNotIn("tickets", first_flight_data)
        self.assertNotIn("taken_places", first_flight_data)

    def test_get_serializer_class_retrieve_action(self):
        url = reverse("airport:flight-detail", args=[self.flight1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("crews", response.data)
        self.assertIn("taken_places", response.data)

        self.assertNotIn("tickets_available", response.data)

        self.assertIn("route", response.data)
        self.assertIn("distance", response.data["route"])

        self.assertIn("airplane", response.data)
        self.assertIn("rows", response.data["airplane"])

    def test_get_serializer_class_create_update_action(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("airport:flight-list")
        data = {
            "route": self.route_london_paris.id,
            "airplane": self.airplane_small.id,
            "departure_time": (timezone.now() + timedelta(days=5, hours=10)).isoformat(),
            "arrival_time": (timezone.now() + timedelta(days=5, hours=12)).isoformat(),
            "crews": [self.crew1.id, self.crew2.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data["route"], int)
        self.assertIsInstance(response.data["airplane"], int)
        self.assertNotIn("tickets_available", response.data)
        self.assertNotIn("crews", response.data)
