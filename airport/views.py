from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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
from airport.serializers import (
    CrewSerializer,
    OrderSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirportSerializer,
    RouteSerializer,
    FlightSerializer,
    TicketSerializer,
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAuthenticated,)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAuthenticated,)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (IsAuthenticated,)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAuthenticated,)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAuthenticated,)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsAuthenticated,)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)
