from django.urls import path

from .views import (CarsView, ComponentView, CreateCarView,
                    CreateComponentView, CreateDealershipView,
                    CreateDealerView, CreateShipmentView, CreateSupportView,
                    CreateTransactionView, IndexView, SupportView,
                    TransactionsView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('new_dealer/', CreateDealerView.as_view(), name="new_dealer"),
    path(
        'new_dealership/',
        CreateDealershipView.as_view(),
        name="create_dealership"
        ),
    # Transactions
    path(
        'dealership/<int:id>/transactions/',
        TransactionsView.as_view(),
        name="get_transactions"
        ),
    path(
        'dealership/<int:id>/transactions/create/',
        CreateTransactionView.as_view(), name="transaction_create"
        ),
    # Components
    path(
        'dealership/<int:id>/components/',
        ComponentView.as_view(),
        name="dealership_components"
        ),
    path(
        'dealership/<int:id>/components/create/',
        CreateComponentView.as_view(),
        name="component_create"
        ),
    # Cars
    path(
        'dealership/<int:id>/cars/',
        CarsView.as_view(),
        name="dealership_cars"
        ),
    path(
        'dealership/<int:id>/cars/create/',
        CreateCarView.as_view(),
        name="cars_create"
        ),

    # Support
    path(
        'dealership/<int:id>/support/',
        SupportView.as_view(),
        name="get_support"
        ),
    path(
        'dealership/<int:id>/support/create/',
        CreateSupportView.as_view(),
        name="new_support"
        ),
    path(
        'dealership/<int:id>/support/shipment/',
        CreateShipmentView.as_view(),
        name="shipment_car"
        ),
]
