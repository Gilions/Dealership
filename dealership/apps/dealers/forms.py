from django.forms import ModelForm

from .models import Car, Component, Dealer, Dealership, Sale, Support


class DelearForm(ModelForm):

    class Meta:
        model = Dealer
        fields = ("title",)


class DealershipForm(ModelForm):

    class Meta:
        model = Dealership
        fields = ("title", "place", )


class CarsForm(ModelForm):

    class Meta:
        model = Car
        fields = (
            "brand", "model", "color", "vin", "price", "markup",)


class ComponentForm(ModelForm):

    class Meta:
        model = Component
        fields = ("title", "quantity", "unit",)


class TransactionForm(ModelForm):

    class Meta:
        model = Sale
        fields = ("buyer", "phone",)


class SupportAddNewForm(ModelForm):

    class Meta:
        model = Support
        fields = (
            "brand", "model", "color", "vin", "discription", "status")


class SupportShipmentForm(ModelForm):

    class Meta:
        model = Support
        fields = ("conclusion", "price", "status")
