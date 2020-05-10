from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from . import models, serializers


class CarViewset(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer
    lookup_fields = ['car-detail', ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance not in models.Car.objects.exclude(reservations=None):
            self.perform_destroy(instance)
            return Response({"Success": "Car deleted."}, status=status.HTTP_200_OK)
        return Response({"Failed": "Cannot be deleted because it contains bookings."}, status=status.HTTP_400_BAD_REQUEST)


class ReservationViewset(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Reservation.objects.all()
    serializer_class = serializers.ReservationSerializer
    lookup_fields = ['reservation-detail', ]
