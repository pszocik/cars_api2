from rest_framework import serializers
from . import models


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Car
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Reservation
        fields = ('id', 'car', 'reserved_by',
                  'reserved_from', 'reserved_to')

    def validate(self, data):
        if models.Reservation.objects.filter(
                reserved_from__range=(data['reserved_from'], data['reserved_to'])) or models.Reservation.objects.filter(
                reserved_to__range=(data['reserved_from'], data['reserved_to'])).filter(car=data['car']):
            raise serializers.ValidationError(
                "There are already some reservations at given date.")

        if data['reserved_from'] > data['reserved_to']:
            raise serializers.ValidationError("Finish must occur after start.")
        if data['reserved_to'] > models.Car.objects.get(name=data['car']).service_date:
            raise serializers.ValidationError(
                "You can't make a reservation after service date.")
        return data
