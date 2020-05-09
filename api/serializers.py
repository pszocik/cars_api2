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
