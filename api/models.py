from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=7)
    service_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Reservation(models.Model):
    reserved_by = models.CharField(max_length=50)
    car = models.ForeignKey(
        Car, related_name='reservations', on_delete=models.CASCADE)
    reserved_from = models.DateTimeField()
    reserved_to = models.DateTimeField()

    def __str__(self):
        return f'{self.reserved_from}-{self.reserved_to}'
