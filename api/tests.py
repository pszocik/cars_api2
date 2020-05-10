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
        models.Car.objects.create(name='S40', brand='Volvo',
                                  registration_number='CXZ11AS', service_date="2020-07-22T19:05:00Z")

    def test_get_car_info(self):
        response = self.client.get('/api/cars/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_car(self):
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

    def test_delete_car(self):
        response = self.client.delete('/api/cars/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Car.objects.count(), 0)

# class ReservationTestCase(APITestCase):

#     def test_reservation_get(self):
#         response = self.client.get('/api/cars/4/reservations/999/')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
