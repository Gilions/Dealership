from rest_framework import serializers

from ..dealers.models import Car, Component, Dealer, Dealership, Sale, Support


class DealerSerializer(serializers.ModelSerializer):
    author = serializers.SlugField('author_username')
    class Meta:
        model = Dealer
        fields = "__all__"


class DealershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealership
        fields = ("id", "title", "place", "profit")


class CarSerializer(serializers.ModelSerializer):
    dealership = serializers.SlugField('dealership_title')
    class Meta:
        model = Car
        exclude = ("author",)


class ComponentSerializer(serializers.ModelSerializer):
    dealership = serializers.SlugField('dealership_title')
    class Meta:
        model = Component
        exclude = ("author",)


class SupportSerializer(serializers.ModelSerializer):
    dealership = serializers.SlugField('dealership_title')
    class Meta:
        model = Support
        exclude = ("author",)


class TransactionsSerializer(serializers.ModelSerializer):
    dealership = serializers.SlugField('dealership_title')
    class Meta:
        model = Sale
        exclude = ("author",)
