import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from . import models
from . import serializers


class CarTestCase(APITestCase):
    def test_api_get(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cars_get(self):
        response = self.client.get('/api/cars/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_car_create(self):
        data = {
            "name": "S40",
            "brand": "Volvo",
            "registration_number": "CXZ11AS",
            "service_date": "2020-07-22T19:05:00Z"
        }
        response = self.client.post('/api/cars/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Car.objects.count(), 1)
        self.assertEqual(models.Car.objects.get().name, 'S40')

    def test_cars_get(self):
        response = self.client.get('/api/cars/1/')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# class ReservationTestCase(APITestCase):

#     def test_reservation_get(self):
#         response = self.client.get('/api/cars/4/reservations/999/')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
