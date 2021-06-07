from django.contrib import admin

from .models import Car, Component, Dealer, Dealership, Sale, Support


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'title', 'author',
    )
    list_filter = ('title',)


@admin.register(Dealership)
class DealershipAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'dealer',
        'title',
        'place',
        'profit'
        )
    list_filter = ('title',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'dealership',
        'brand',
        'model',
        'color',
        'vin',
        'pub_date',
        'price',
        'markup',
        'cost'
        )


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = (
        'dealership',
        'title',
        'quantity',
        'unit',
        )


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        'dealership',
        'brand',
        'model',
        'color',
        'vin',
        'pub_date',
        'profit',
        'buyer',
        'phone'
        )


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = (
        'dealership',
        'brand',
        'model',
        'color',
        'vin',
        'pub_date',
        'discription',
        'shipment',
        'conclusion',
        'price',
        'status'
        )
