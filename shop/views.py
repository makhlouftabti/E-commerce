from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from .forms import *
import requests
import inspect
from django.conf import settings


# Create your views here.
def index(request):
    context = {}
    return render(request, "index.html")


def clothes(request):
    items = Product.objects.all()

    context = {
        "items": items,
    }
    return render(request, "clothes.html", context)


def accessories(request):
    return render(request, "accessories.html")


def cart(request, id):
    user = User.objects.get(pk=id)
    customer = Customer.objects.get(user=user)
    cart = Cart.objects.get(customer=customer)
    cartitem = CartItem.objects.filter(cart=cart)
    count = cartitem.count()
    items = [item.product for item in cartitem]

    context = {
        "count": count,
        "items": items,
    }
    return render(request, "cart.html", context)


# Add Item to the cart
def AddToCart(request, item_id):
    product = get_object_or_404(Product, id=item_id)
    if request.user.is_authenticated:
        user = request.user
        customer = get_object_or_404(Customer, user=user)
        cart = get_object_or_404(Cart, customer=customer)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, "The Item is added to your cart")
        return redirect("clothes")
    else:
        return redirect("login")


# delete
def DeleteItem(request, item_id):
    product = get_object_or_404(Product, id=item_id)
    cart_item = CartItem.objects.get(product=product)
    cart_item.delete()
    return redirect("clothes")


def register(request):
    form = CreateNewUser()
    if request.method == "POST":
        form = CreateNewUser(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, username + " Created Successfully !")
            return redirect("login")
        else:
            messages.error(request, " Something did not go as planned !")
    context = {"form": form}

    return render(request, "register.html", context)


def userlogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Credentials error")

    context = {}

    return render(request, "login.html", context)


def userLogout(request):
    logout(request)
    return redirect("index")


def send_email(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            email = request.user.email
        else:
            email = request.POST.get("email", "")

        comments = request.POST.get("comments", "")

        if email and comments:
            subject1 = "Comment from a client"
            message1 = f"User's Email: {email}\nComment: {comments}"
            from_email = "djtest1210@gmail.com"
            recipient_list = ["djtest1210@gmail.com"]
            send_mail(
                subject1, message1, from_email, recipient_list, fail_silently=False
            )
            return render(request, "send_email.html")  # Redirect to a success page
        else:
            messages.error(request, "Please provide a valid email and comment.")

    return render(request, "index.html")


def search(request):
    if request.method == "GET":
        search = request.GET.get("searchBox", "")
        results = Product.objects.filter(
            Q(name__icontains=search) | Q(brand__name__icontains=search)
        )
        context = {"items": results}
    return render(request, "search.html", context)
