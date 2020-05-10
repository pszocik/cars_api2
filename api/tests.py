import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from . import models
from . import serializers


class CarTestCase(APITestCase):
    def test_get_cars(self):
        response = self.client.get('/api/cars/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def setUp(self):
        volvo = models.Car.objects.create(name='S40', brand='Volvo',
                                          registration_number='CXZ11AS', service_date="2020-07-22T19:05:00Z")
        models.Reservation.objects.create(
            car=volvo, reserved_by='Mike', reserved_from='2020-02-22T22:22:00Z', reserved_to='2020-02-24T22:22:00Z')

    def test_get_car_info(self):
        response = self.client.get('/api/cars/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_car(self):
        response = self.client.get('/api/cars/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_car(self):
        data = {
            "name": "Punto",
            "brand": "Fiat",
            "registration_number": "NOL13S1",
            "service_date": "2020-07-22T15:05:00Z",
        }
        response = self.client.put('/api/cars/1/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_car_with_reservation(self):
        response = self.client.delete('/api/cars/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(models.Car.objects.count(), 1)


class ReservationTestCase(APITestCase):

    def setUp(self):
        fiesta = models.Car.objects.create(name='Fiesta', brand='Ford',
                                           registration_number='ABC1234', service_date="2020-06-22T19:05:00Z")
        models.Reservation.objects.create(
            car=fiesta, reserved_by='John', reserved_from='2020-02-22T22:22:00Z', reserved_to='2020-02-24T22:22:00Z')

    def test_get_invalid_reservation(self):
        response = self.client.get('/api/cars/1/reservations/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_reservation_info(self):
        response = self.client.get('/api/cars/1/reservations/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_car(self):
        data = {
            "car": 1,
            "reserved_by": "John Smith",
            "reserved_from": "2020-02-20T12:20:00Z",
            "reserved_to": "2020-02-21T16:20:00Z",
        }
        response = self.client.put('/api/cars/1/reservations/1/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_reservation(self):
        response = self.client.delete('/api/cars/1/reservations/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Reservation.objects.count(), 0)
