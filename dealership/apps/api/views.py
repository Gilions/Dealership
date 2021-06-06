from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from ..dealers.models import Dealer, Dealership
from .permissions import CustomPermission
from .serializers import (CarSerializer, ComponentSerializer, DealerSerializer,
                          DealershipSerializer, SupportSerializer,
                          TransactionsSerializer)


class DealerViewSet(viewsets.ModelViewSet):
    """
    Таблица: Dealer
    Допустимые методы:
    GET, POST, PUT, PATCH, DELETE
    """
    serializer_class = DealerSerializer
    permission_classes = (CustomPermission,)

    def get_queryset(self):
        dealer = get_object_or_404(
            Dealer,
            author=self.request.user
        )
        answer = []
        answer.append(dealer)
        return answer


class DealershipViewSet(viewsets.ModelViewSet):
    """
    Таблица: Dealership
    Допустимые методы:
    GET, POST, PUT, PATCH, DELETE
    """
    serializer_class = DealershipSerializer
    permission_classes = (CustomPermission,)

    def get_queryset(self):
            dealer = get_object_or_404(
                Dealer,
                author=self.request.user
            )
            return dealer.dealership.all()


class CarViewSet(viewsets.ModelViewSet):
    """
    Таблица: Car
    Допустимые методы:
    GET, POST, PUT, PATCH, DELETE
    """
    serializer_class = CarSerializer
    permission_classes = (CustomPermission,)

    def get_queryset(self):
        dealership = get_object_or_404(
            Dealership,
            id=self.kwargs.get("dealer_id")
        )
        return dealership.cars.all()


class ComponentViewSet(viewsets.ModelViewSet):
    """
    Таблица: Component
    Допустимые методы:
    GET, POST, PUT, PATCH, DELETE
    """
    serializer_class = ComponentSerializer
    permission_classes = (CustomPermission,)

    def get_queryset(self):
        dealership = get_object_or_404(
            Dealership,
            id=self.kwargs.get("dealer_id")
        )
        return dealership.components.all()


class SupportViewSet(viewsets.ModelViewSet):
    """
    Таблица: Support
    Допустимые методы:
    GET, POST, PUT, PATCH, DELETE
    """
    serializer_class = SupportSerializer
    permission_classes = (CustomPermission,)

    def get_queryset(self):
        dealership = get_object_or_404(
            Dealership,
            id=self.kwargs.get("dealer_id")
        )
        return dealership.supported.all()


class TransactionsViewSet(viewsets.ModelViewSet):
    """
    Таблица: Sale
    Допустимые методы:
    GET, POST, PUT, PATCH, DELETE
    """
    serializer_class = TransactionsSerializer
    permission_classes = (CustomPermission,)

    def get_queryset(self):
        dealership = get_object_or_404(
            Dealership,
            id=self.kwargs.get("dealer_id")
        )
        return dealership.sales.all()