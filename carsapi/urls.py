from rest_framework import routers
from rest_framework_extensions.routers import NestedRouterMixin
from api import views
from django.urls import include, path
from django.contrib import admin


class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    pass


router = NestedDefaultRouter()
cars = router.register(r'cars', views.CarViewset)
cars.register(
    r'reservations',
    views.ReservationViewset,
    basename='car-reservation',
    parents_query_lookups=['car']
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
