from django.urls import path

from .views import (get_cars, get_component, get_support, get_transactions,
                    index, new_cars, new_component, new_dealer, new_dealership,
                    new_support, new_transaction, shipment_car)

urlpatterns = [
    path('', index, name='index'),
    path('new_dealer/', new_dealer, name="new_dealer"),
    path('new_dealership/', new_dealership, name="create_dealership"),
    # Transactions
    path('dealership/<int:id>/transactions/', get_transactions, name="get_transactions"),
    path('dealership/<int:id>/transactions/create/', new_transaction, name="transaction_create"),
    # Components
    path('dealership/<int:id>/components/', get_component, name="dealership_components"),
    path('dealership/<int:id>/components/create/', new_component, name="component_create"),
    # Cars
    path('dealership/<int:id>/cars/', get_cars, name="dealership_cars"),
    path('dealership/<int:id>/cars/create/', new_cars, name="cars_create"),

    # Support
    path('dealership/<int:id>/support/', get_support, name="get_support"),
    path('dealership/<int:id>/support/create/', new_support, name="new_support"),
    path('dealership/<int:id>/support/shipment/', shipment_car, name="shipment_car"),
]