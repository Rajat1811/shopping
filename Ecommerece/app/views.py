from http.client import NETWORK_AUTHENTICATION_REQUIRED
from itertools import product
from re import U
from unicodedata import category
from urllib import request
from django.shortcuts import render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages


class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category="TW")
        bottomwears = Product.objects.filter(category="BW")
        mobiles = Product.objects.filter(category="M")

        return render(
            request,
            "app/home.html",
            {"topwears": topwears, "bottomwears": bottomwears, "mobiles": mobiles},
        )


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html", {"product": product})


def add_to_cart(request):
    return render(request, "app/addtocart.html")


def buy_now(request):
    return render(request, "app/buynow.html")


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, "app/address.html", {"add": add, "active": "btn-primary"})


def orders(request):
    return render(request, "app/orders.html")


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category="M")
    elif data == "iPhone" or data == "Oppo" or data == "Nokia":
        mobiles = Product.objects.filter(category="M").filter(brand=data)
    elif data == "below":
        mobiles = Product.objects.filter(category="M").filter(
            discounted_price__lt=20000
        )
    elif data == "above":
        mobiles = Product.objects.filter(category="M").filter(
            discounted_price__gt=20000
        )
    return render(request, "app/mobile.html", {"mobiles": mobiles})


def topwear(request):
    topwears = Product.objects.filter(category="TW")
    return render(request, "app/topwear.html", {"topwears": topwears})


def bottomwear(request):
    bottomwears = Product.objects.filter(category="BW")
    return render(request, "app/bottomwear.html", {"bottomwears": bottomwears})


class CustomRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", {"form": form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations!! RegisteredSuccessfully")
            form.save()
        return render(request, "app/customerregistration.html", {"form": form})


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(
            request, "app/profile.html", {"form": form, "active": "btn-primary"}
        )

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data["name"]
            locality = form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            zipcode = form.cleaned_data["zipcode"]
            reg = Customer(
                user=user,
                name=name,
                locality=locality,
                city=city,
                state=state,
                zipcode=zipcode,
            )
            reg.save()
            messages.success(request, "Congratulations!! Profile Updated Successfully")
        return render(
            request, "app/profile.html", {"form": form, "active": "btn-primary"}
        )


def checkout(request):
    return render(request, "app/checkout.html")
