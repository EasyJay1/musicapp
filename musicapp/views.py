
from django.conf import settings

from django.core.mail import send_mail
from django.http import HttpResponse

from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem
from django.http import JsonResponse
import json
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import OrderForm, CreateUserForm

def registerPage(request):
    if request.user.is_authenticated:
        return  redirect('index')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account created for ' + user + " successful")
                return redirect('login')

        context = {'form':form}
        return render(request, 'register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user) # Add this line to log in the user
                return redirect('index')
            else:
                messages.info(request, 'Username Or Password is incorrect')

        context = {}
        return render(request, 'login.html', context)

def contact(request):
    if request.method == 'POST':
        # Process the form submission here
        # ...
        return render(request, 'contact_success.html')
    else:
        return render(request, 'contact.html')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()

        num_of_item = cart.num_of_items

        print(cartitem)
    return JsonResponse(num_of_item, safe=False)

def artist_view(request):
    return render(request, 'artist.html')

def emptysample_view(request):
    return render(request, 'emptysample.html')



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send email
        subject = f"Contact Form Submission from {name}"
        message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['michaelglory723@gmail.com'])

        # Optionally, you can redirect the user to a success page
        return render(request, 'success.html')

    return render(request, 'contact.html')
@login_required(login_url='login')
# Create your views here.
def index(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)

    else:
        cartitems = []
        cart = {"get_cart_total": 0, "get_itemtotal": 0}

    products = Product.objects.all()
    return render(request, 'index.html', {'products': products, 'cart':cart})

@login_required(login_url='login')
def cart(request):
    cart = None
    cartitems = []

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitems = cart.cartitems.all()

    context = {"cart":cart, "items":cartitems}
    return render(request, "cart.html", context)

@login_required(login_url='login')
def confirm_payment(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.completed = True
    cart.save()
    messages.success(request, "Payment made successfully")
    return redirect("index")
