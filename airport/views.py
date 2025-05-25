from django.db.models import F, Count
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

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
from airport.permissions import IsAdminOrReadOnly
from airport.serializers import (
    CrewSerializer,
    OrderSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirportSerializer,
    RouteSerializer,
    FlightSerializer,
    TicketSerializer,
    OrderListSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    TicketListSerializer,
    CrewImageSerializer,
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "upload_image":
            return CrewImageSerializer
        return CrewSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[
            IsAdminUser,
        ],
    )
    def upload_image(self, request, pk=None):
        crew = self.get_object()
        serializer = self.get_serializer(crew, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().order_by("-created_at")
        return Order.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrReadOnly,)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all().select_related("airplane_type")
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneDetailSerializer
        return AirplaneSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        name = self.request.query_params.get("name")
        closest_big_city = self.request.query_params.get("closest_big_city")
        if name:
            self.queryset = self.queryset.filter(name__icontains=name)
        if closest_big_city:
            self.queryset = self.queryset.filter(
                closest_big_city__icontains=closest_big_city
            )
        return self.queryset


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer

    def get_queryset(self):
        queryset = (
            self.queryset.select_related(
                "route", "route__source", "route__destination", "airplane"
            )
            .prefetch_related(
                "crews", "tickets"
            )
            .annotate(
                tickets_available=(
                    F("airplane__rows") * F("airplane__seats_in_row") - Count("tickets")
                )
            )
        )

        route = self.request.query_params.get("route")
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")

        if route:
            route_id = int(route)
            queryset = queryset.filter(route__id=route_id)
        if source:
            queryset = queryset.filter(
                route__source__closest_big_city__icontains=source
            )
        if destination:
            queryset = queryset.filter(
                route__destination__closest_big_city__icontains=destination
            )
        return queryset.distinct()


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        return TicketSerializer
