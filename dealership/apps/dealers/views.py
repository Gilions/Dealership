import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, ListView
from django.views.generic.edit import UpdateView

from .forms import (CarsForm, ComponentForm, DealershipForm, DelearForm,
                    SupportAddNewForm, SupportShipmentForm, TransactionForm)
from .models import Car, Component, Dealer, Dealership, Sale, Support


class IndexView(LoginRequiredMixin, ListView):
    model = Dealer
    template_name = "index.html"
    context_object_name = "dealership"

    def get(self, request, *args, **kwargs):
        check = Dealer.objects.filter(author=self.request.user).exists()
        if check:
            return super().get(request, *args, **kwargs)
        return redirect("new_dealer")

    def get_queryset(self):
        dealer = get_object_or_404(
            Dealer,
            author=self.request.user
        )
        return dealer.dealership.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dealer = get_object_or_404(
            Dealer,
            author=self.request.user
        )
        context["dealer"] = dealer
        return context


class ComponentView(LoginRequiredMixin, ListView):
    model = Component
    template_name = "components.html"
    context_object_name = "components"

    def get_queryset(self):
        dealership = get_object_or_404(
            Dealership,
            id=self.kwargs.get("id")
        )
        return dealership.components.all()

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        context["dealer"] = get_object_or_404(
            Dealership, id=self.kwargs.get("id"))
        return context


class TransactionsView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = "transactions.html"
    context_object_name = "sales"

    def get_queryset(self):
        dealership = get_object_or_404(
            Dealership,
            id=self.kwargs.get("id")
        )
        return dealership.sales.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dealer = get_object_or_404(
            Dealership,
            id=self.kwargs.get("id")
        )
        context["dealer"] = dealer
        return context


class CarsView(LoginRequiredMixin, ListView):
    model = Car
    template_name = "cars.html"
    context_object_name = "cars"

    def get_queryset(self):
        dealership = get_object_or_404(
            Dealership,
            id=self.kwargs.get("id")
        )
        return dealership.cars.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dealer = get_object_or_404(
            Dealership,
            id=self.kwargs.get("id")
        )
        context["dealer"] = dealer
        return context


class SupportView(LoginRequiredMixin, ListView):
    model = Support
    template_name = "support.html"
    context_object_name = "support"

    def get_queryset(self):
        dealership = get_object_or_404(
            Dealership,
            id=self.kwargs.get("id")
        )
        return dealership.supported.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dealer = get_object_or_404(
            Dealership,
            id=self.kwargs.get("id")
        )
        context["dealer"] = dealer
        return context


class CreateCarView(LoginRequiredMixin, CreateView):
    model = Car
    form_class = CarsForm
    template_name = "form_item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["car"] = True
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.dealership = get_object_or_404(
            Dealership,
            id=self.kwargs.get("id")
        )
        form.save()
        return redirect("dealership_cars", id=self.kwargs.get("id"))


class CreateComponentView(LoginRequiredMixin, CreateView):
    model = Component
    form_class = ComponentForm
    template_name = "form_item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["component"] = True
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.dealership = get_object_or_404(
            Dealership,
            id=self.kwargs.get("id")
        )
        form.save()
        return redirect("dealership_components", id=self.kwargs.get("id"))


class CreateDealerView(LoginRequiredMixin, CreateView):
    model = Dealer
    form_class = DelearForm
    template_name = "form_dealer.html"

    def get(self, request, *args, **kwargs):
        check = Dealer.objects.filter(author=self.request.user).exists()
        if check:
            return redirect("index")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect("index")


class CreateDealershipView(LoginRequiredMixin, CreateView):
    model = Dealership
    form_class = DealershipForm
    template_name = "form_dealer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_dealership"] = True
        return context

    def form_valid(self, form):
        form.instance.dealer = get_object_or_404(
            Dealer,
            author=self.request.user
        )
        form.instance.author = self.request.user
        form.save()
        return redirect("index")


class CreateTransactionView(LoginRequiredMixin, CreateView):
    model = Sale
    form_class = TransactionForm
    template_name = "form_item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sale"] = True
        return context

    def form_valid(self, form):
        car = get_object_or_404(Car, id=self.kwargs.get("id"))
        form.instance.dealership = car.dealership
        form.instance.brand = car.brand
        form.instance.model = car.model
        form.instance.color = car.color
        form.instance.vin = car.vin
        form.instance.profit = car.cost - car.price
        form.instance.author = self.request.user
        form.save()

        dealership = car.dealership
        dealership.profit = car.cost - car.price
        dealership.save()
        car.delete()
        return redirect("get_transactions", id=dealership.id)


class CreateSupportView(LoginRequiredMixin, CreateView):
    model = Support
    form_class = SupportAddNewForm
    template_name = "form_item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["support"] = True
        return context

    def form_valid(self, form):
        dealership = get_object_or_404(Dealership, id=self.kwargs.get("id"))
        form.instance.dealership = dealership
        form.instance.author = self.request.user
        form.save()
        return redirect("get_support", id=self.kwargs.get("id"))


class CreateShipmentView(LoginRequiredMixin, UpdateView):
    model = Support
    form_class = SupportShipmentForm
    template_name = "form_item.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Support, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shipment"] = True
        return context

    def form_valid(self, form):
        form.instance.shipment = datetime.datetime.now()
        form.save()

        car = get_object_or_404(
            Support,
            id=self.kwargs.get("id")
        )
        dealership = car.dealership
        dealership.profit += form.instance.price
        dealership.save()
        return redirect("get_support", id=dealership.id)
