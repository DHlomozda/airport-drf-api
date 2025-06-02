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
from airport.schemas.airplane_schema import (
    airplane_list_schema,
    airplane_create_schema,
    airplane_retrieve_schema,
    airplane_update_schema,
    airplane_partial_update_schema,
    airplane_destroy_schema
)
from airport.schemas.airplane_type_schema import (
    airplane_type_partial_update_schema,
    airplane_type_update_schema,
    airplane_type_destroy_schema,
    airplane_type_retrieve_schema,
    airplane_type_create_schema,
    airplane_type_list_schema
)
from airport.schemas.airport_schema import (
    airport_list_schema,
    airport_create_schema,
    airport_retrieve_schema,
    airport_update_schema,
    airport_partial_update_schema,
    airport_destroy_schema
)
from airport.schemas.crew_schema import (
    crew_upload_image_schema,
    crew_list_schema,
    crew_create_schema,
    crew_retrieve_schema,
    crew_update_schema,
    crew_partial_update_schema,
    crew_delete_schema
)
from airport.schemas.flight_schema import (
    flight_list_schema,
    flight_create_schema,
    flight_retrieve_schema,
    flight_update_schema,
    flight_partial_update_schema,
    flight_destroy_schema
)
from airport.schemas.order_schema import (
    order_list_schema,
    order_create_schema,
    order_retrieve_schema
)
from airport.schemas.route_schema import (
    route_destroy_schema,
    route_partial_update_schema,
    route_update_schema,
    route_retrieve_schema,
    route_create_schema,
    route_list_schema
)
from airport.schemas.ticket_schema import (
    ticket_list_schema,
    ticket_create_schema,
    ticket_retrieve_schema,
    ticket_update_schema,
    ticket_partial_update_schema,
    ticket_destroy_schema
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

    @crew_list_schema
    def list(self, request, *args, **kwargs):
        """
        Retrieves a list of all crews.
        """
        return super().list(request, *args, **kwargs)

    @crew_create_schema
    def create(self, request, *args, **kwargs):
        """
        Creates a new crew. Only accessible to administrators.
        """
        return super().create(request, *args, **kwargs)

    @crew_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves details of a specific crew by ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @crew_update_schema
    def update(self, request, *args, **kwargs):
        """
        Updates all fields of a specific crew by ID.
        """
        return super().update(request, *args, **kwargs)

    @crew_partial_update_schema
    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates some fields of a specific crew by ID.
        """
        return super().partial_update(request, *args, **kwargs)

    @crew_delete_schema
    def destroy(self, request, *args, **kwargs):
        """
        Deletes a specific crew by ID.
        """
        return super().destroy(request, *args, **kwargs)

    @crew_upload_image_schema
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

    @order_list_schema
    def list(self, request, *args, **kwargs):
        """
        Retrieves a list of all orders.
        """
        return super().list(request, *args, **kwargs)

    @order_create_schema
    def create(self, request, *args, **kwargs):
        """
        Creates a new order. Only accessible to administrators.
        """
        return super().create(request, *args, **kwargs)

    @order_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves details of a specific order by ID.
        """
        return super().retrieve(request, *args, **kwargs)



class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @airplane_type_list_schema
    def list(self, request, *args, **kwargs):
        """
        Retrieves a list of all airplane_type.
        """
        return super().list(request, *args, **kwargs)

    @airplane_type_create_schema
    def create(self, request, *args, **kwargs):
        """
        Creates a new airplane_type. Only accessible to administrators.
        """
        return super().create(request, *args, **kwargs)

    @airplane_type_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves details of a specific airplane_type by ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @airplane_type_update_schema
    def update(self, request, *args, **kwargs):
        """
        Updates all fields of a specific airplane_type by ID.
        """
        return super().update(request, *args, **kwargs)

    @airplane_type_partial_update_schema
    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates some fields of a specific airplane_type by ID.
        """
        return super().partial_update(request, *args, **kwargs)

    @airplane_type_destroy_schema
    def destroy(self, request, *args, **kwargs):
        """
        Deletes a specific airplane_type by ID.
        """
        return super().destroy(request, *args, **kwargs)


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

    @airplane_list_schema
    def list(self, request, *args, **kwargs):
        """
        Retrieves a list of airplanes.
        Uses AirplaneListSerializer for list representation.
        """
        return super().list(request, *args, **kwargs)

    @airplane_create_schema
    def create(self, request, *args, **kwargs):
        """
        Creates a new airplane.
        Only administrators are allowed.
        """
        return super().create(request, *args, **kwargs)

    @airplane_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves details of a specific airplane by ID.
        Uses AirplaneDetailSerializer for detailed representation.
        """
        return super().retrieve(request, *args, **kwargs)

    @airplane_update_schema
    def update(self, request, *args, **kwargs):
        """
        Fully updates an existing airplane.
        Only administrators are allowed.
        """
        return super().update(request, *args, **kwargs)

    @airplane_partial_update_schema
    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates selected fields of an airplane.
        Only administrators are allowed.
        """
        return super().partial_update(request, *args, **kwargs)

    @airplane_destroy_schema
    def destroy(self, request, *args, **kwargs):
        """
        Deletes an airplane by ID.
        Only administrators are allowed.
        """
        return super().destroy(request, *args, **kwargs)


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

    @airport_list_schema
    def list(self, request, *args, **kwargs):
        """
        Retrieves a list of airports.
        Supports filtering by name and closest_big_city.
        """
        return super().list(request, *args, **kwargs)

    @airport_create_schema
    def create(self, request, *args, **kwargs):
        """
        Creates a new airport.
        Only administrators are allowed.
        """
        return super().create(request, *args, **kwargs)

    @airport_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves details of a specific airport by ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @airport_update_schema
    def update(self, request, *args, **kwargs):
        """
        Fully updates an existing airport.
        Only administrators are allowed.
        """
        return super().update(request, *args, **kwargs)

    @airport_partial_update_schema
    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates selected fields of an airport.
        Only administrators are allowed.
        """
        return super().partial_update(request, *args, **kwargs)

    @airport_destroy_schema
    def destroy(self, request, *args, **kwargs):
        """
        Deletes an airport by ID.
        Only administrators are allowed.
        """
        return super().destroy(request, *args, **kwargs)

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

    @route_list_schema
    def list(self, request, *args, **kwargs):
        """
        Retrieves a list of routes.
        Supports filtering by name and closest_big_city.
        """
        return super().list(request, *args, **kwargs)

    @route_create_schema
    def create(self, request, *args, **kwargs):
        """
        Creates a new route.
        Only administrators are allowed.
        """
        return super().create(request, *args, **kwargs)

    @route_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves details of a specific route by ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @route_update_schema
    def update(self, request, *args, **kwargs):
        """
        Fully updates an existing route.
        Only administrators are allowed.
        """
        return super().update(request, *args, **kwargs)

    @route_partial_update_schema
    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates selected fields of a route.
        Only administrators are allowed.
        """
        return super().partial_update(request, *args, **kwargs)

    @route_destroy_schema
    def destroy(self, request, *args, **kwargs):
        """
        Deletes a route by ID.
        Only administrators are allowed.
        """
        return super().destroy(request, *args, **kwargs)


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

    @flight_list_schema
    def list(self, request, *args, **kwargs):
        """
        Retrieves a list of all flights.
        """
        return super().list(request, *args, **kwargs)

    @flight_create_schema
    def create(self, request, *args, **kwargs):
        """
        Creates a new flight. Only accessible to administrators.
        """
        return super().create(request, *args, **kwargs)

    @flight_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves details of a specific flight by ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @flight_update_schema
    def update(self, request, *args, **kwargs):
        """
        Updates all fields of a specific flight by ID.
        """
        return super().update(request, *args, **kwargs)

    @flight_partial_update_schema
    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates some fields of a specific flight by ID.
        """
        return super().partial_update(request, *args, **kwargs)

    @flight_destroy_schema
    def destroy(self, request, *args, **kwargs):
        """
        Deletes a specific flight by ID.
        """
        return super().destroy(request, *args, **kwargs)

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

    @ticket_list_schema
    def list(self, request, *args, **kwargs):
        """
        Retrieves a list of all tickets.
        """
        return super().list(request, *args, **kwargs)

    @ticket_create_schema
    def create(self, request, *args, **kwargs):
        """
        Creates a new ticket. Only accessible to administrators.
        """
        return super().create(request, *args, **kwargs)

    @ticket_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves details of a specific ticket by ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @ticket_update_schema
    def update(self, request, *args, **kwargs):
        """
        Updates all fields of a specific ticket by ID.
        """
        return super().update(request, *args, **kwargs)

    @ticket_partial_update_schema
    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates some fields of a specific ticket by ID.
        """
        return super().partial_update(request, *args, **kwargs)

    @ticket_destroy_schema
    def destroy(self, request, *args, **kwargs):
        """
        Deletes a specific ticket by ID.
        """
        return super().destroy(request, *args, **kwargs)
