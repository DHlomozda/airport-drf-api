from rest_framework import serializers

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


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "created_at", "user")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = (
            "id",
            "name",
        )


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "seat_in_row", "airplane_type")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(attrs["row"], attrs["seat"], attrs["airplane"])
        return data
