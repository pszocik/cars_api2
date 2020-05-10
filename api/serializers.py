from rest_framework import serializers
from django.http import HttpRequest as request
from . import models

BASE_URL = "http://127.0.0.1:8000/"


class CarSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='car-detail', read_only=True)
    reservations = serializers.SerializerMethodField('get_reservations')

    class Meta:
        model = models.Car
        fields = ('name', 'brand', 'registration_number',
                  'service_date', 'url', 'reservations')

    def get_reservations(self, obj):
        return f"{BASE_URL}api/cars/{obj.id}/reservations/"


class ReservationSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_url')

    class Meta:
        model = models.Reservation
        fields = ('id', 'car', 'reserved_by',
                  'reserved_from', 'reserved_to', 'url')

    def validate(self, data):
        if models.Reservation.objects.filter(
                reserved_from__range=(data['reserved_from'], data['reserved_to'])) or models.Reservation.objects.filter(
                reserved_to__range=(data['reserved_from'], data['reserved_to'])).filter(car=data['car']):
            if self.context['request'].method == 'POST':
                raise serializers.ValidationError({'reservation_date':
                                                   "There are already some reservations at given date."})

        if data['reserved_from'] > data['reserved_to']:
            raise serializers.ValidationError("Finish must occur after start.")
        if data['reserved_to'] > models.Car.objects.get(name=data['car']).service_date:
            raise serializers.ValidationError(
                "You can't make a reservation after service date.")
        return data

    def get_url(self, obj):
        id = models.Car.objects.get(name=obj).id
        return f"{BASE_URL}api/cars/{id}/reservations/{obj.id}"
