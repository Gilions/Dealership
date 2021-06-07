from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CarViewSet, ComponentViewSet, DealershipViewSet,
                    DealerViewSet, SupportViewSet, TransactionsViewSet)

rounter_v1 = DefaultRouter()
rounter_v1.register(
    'dealer',
    DealerViewSet,
    basename="dealer_api"
    )
rounter_v1.register(
    'dealership',
    DealershipViewSet,
    basename="dealership_api"
    )
rounter_v1.register(
    r'dealership/(?P<dealer_id>\d+)/cars',
    CarViewSet,
    basename="cars_api"
    )
rounter_v1.register(
    r'dealership/(?P<dealer_id>\d+)/components',
    ComponentViewSet,
    basename="component_api"
    )
rounter_v1.register(
    r'dealership/(?P<dealer_id>\d+)/transactions',
    TransactionsViewSet,
    basename="transactions_api"
    )
rounter_v1.register(
    r'dealership/(?P<dealer_id>\d+)/supports',
    SupportViewSet,
    basename="supports_api"
    )


urlpatterns = [
    path('v1/', include(rounter_v1.urls)),
]
