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

app_name = "airport_api"

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("orders", OrderViewSet)
router.register("airplaneTypes", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("flights", FlightViewSet)
router.register("tickets", TicketViewSet)


urlpatterns = [path("", include(router.urls))]
