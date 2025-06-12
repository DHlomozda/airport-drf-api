from django.urls import path, include
from rest_framework import routers

from airport.views import (
    CrewViewSet,
    OrderViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    AirportViewSet,
    RouteViewSet,
    FlightViewSet,
    TicketViewSet,
)

app_name = "airport"

router = routers.DefaultRouter()
router.register("crews", CrewViewSet, basename="crew")
router.register("orders", OrderViewSet, basename="order")
router.register(
    "airplaneTypes",
    AirplaneTypeViewSet,
    basename="airplaneTypes"
)
router.register("airplanes", AirplaneViewSet, basename="airplane")
router.register("airports", AirportViewSet, basename="airport")
router.register("routes", RouteViewSet, basename="route")
router.register("flights", FlightViewSet, basename="flight")
router.register("tickets", TicketViewSet, basename="ticket")


urlpatterns = [path("", include(router.urls))]
