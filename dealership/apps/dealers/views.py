import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (CarsForm, ComponentForm, DealershipForm, DelearForm,
                    SupportAddNewForm, SupportShipmentForm, TransactionForm)
from .models import Car, Component, Dealer, Dealership, Support


@login_required
def index(request):
    check = Dealer.objects.filter(author=request.user).exists()
    if check:
        dealer = get_object_or_404(Dealer, author=request.user)
        dealership = dealer.dealership.all()
        context = {
            "dealer": dealer,
            "dealership": dealership
        }
        return render(request, 'index.html', context)
    return redirect("new_dealer")


@login_required
def get_component(request, id):
    dealer = get_object_or_404(
        Dealership,
        id=id
    )
    components = dealer.components.all()
    context = {
        "dealer": dealer,
        "components": components,
    }
    return render (request, "components.html", context)


@login_required
def get_transactions(request, id):
    dealer = get_object_or_404(
        Dealership,
        id=id
    )
    sales = dealer.sales.all()
    context = {
        "sales": sales,
        "dealer": dealer
    }
    return render(request, "transactions.html", context)


@login_required
def get_cars(request, id):
    dealer = get_object_or_404(
        Dealership,
        id=id
    )
    cars = dealer.cars.all()
    context = {
        "dealer": dealer,
        "cars": cars,
    }
    return render (request, "cars.html", context)


@login_required
def get_support(request, id):
    dealer = get_object_or_404(
        Dealership,
        id=id
    )
    support = dealer.supported.all()
    context = {
        "dealer": dealer,
        "support": support,
    }
    return render (request, "support.html", context)


@login_required
def new_cars(request, id):
    # Create a new car
    form = CarsForm(request.POST, files=request.FILES or None)
    if form.is_valid():
        new_car = form.save(commit=False)
        new_car.dealership = get_object_or_404(
            Dealership,
            id=id
        )
        new_car.author = request.user
        new_car.save()
        return redirect("dealership_cars", id=id)
    context = {
        "form": form,
        "car": True
        }
    return render(request, "form_item.html", context)


@login_required
def new_component(request, id):
    # Crate a new component
    component = True
    form = ComponentForm(request.POST, files=request.FILES or None)
    if form.is_valid():
        new_component = form.save(commit=False)
        new_component.dealership = get_object_or_404(
            Dealership,
            id=id
        )
        new_component.author = request.user
        new_component.save()
        return redirect("dealership_components", id=id)

    context = {
        "component": component,
        "form": form

    }
    return render(request, "form_item.html", context)


@login_required
def new_dealer(request):
    # Create a new dealer
    form = DelearForm(request.POST, files=request.FILES or None)
    if form.is_valid():
        new_dealer = form.save(commit=False)
        new_dealer.author = request.user
        new_dealer.save()
        return redirect("index")
    context = {
        "form": form
    }
    return render(request, "form_dealer.html", context)


@login_required
def new_dealership(request):
    # Create a new dealership
    form = DealershipForm(request.POST, files=request.FILES or None)
    if form.is_valid():
        new_dealer_center = form.save(commit=False)
        new_dealer_center.dealer = get_object_or_404(
            Dealer,
            author = request.user
        )
        new_dealer_center.author = request.user
        new_dealer_center.save()
        return redirect("index")
    context = {
        "new_dealership": True,
        "form": form
    }
    return render(request, "form_dealer.html", context)


@login_required
def new_transaction(request, id):
    form = TransactionForm()
    if request.method == "POST":
        form = TransactionForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            car = get_object_or_404(Car, id=id)
            new_sale = form.save(commit=False)
            new_sale.dealership = car.dealership
            new_sale.brand = car.brand
            new_sale.model = car.model
            new_sale.color = car.color
            new_sale.vin = car.vin
            new_sale.profit = car.cost - car.price
            new_sale.author = request.user
            new_sale.save()

            dealership = car.dealership
            dealership.profit += car.cost - car.price
            dealership.save()
            car.delete()
            return redirect("get_transactions", id=dealership.id)
    context = {
        "form": form,
        "sale": True
    }
    return render(request, "form_item.html", context)


@login_required
def new_support(request, id):
    form = SupportAddNewForm(request.POST, files=request.FILES or None)
    if form.is_valid():
        new_support = form.save(commit=False)
        new_support.dealership = get_object_or_404(
                Dealership,
                id=id
            )
        new_support.author = request.user
        new_support.save()
        return redirect("get_support", id=id)
    context = {
        "form": form,
        "support": True
    }
    return render(request, "form_item.html", context)


@login_required
def shipment_car(request, id):
    car = get_object_or_404(
            Support,
            id=id
        )
    form = SupportShipmentForm()
    if request.method == "POST":
        form = SupportShipmentForm(request.POST, files=request.FILES or None, instance=car)
        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.shipment = datetime.datetime.now()
            shipment.save()

            dealership = car.dealership
            dealership.profit += shipment.price
            dealership.save()
            return redirect("get_support", id=dealership.id)
    context = {
        "form": form,
        "shipment": True
    }
    return render(request, "form_item.html", context)
