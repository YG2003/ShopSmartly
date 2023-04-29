from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
import lxml
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ItemsTracked, User
from django.conf import settings
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler

# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserRegistartionForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account Created for {username}!!")
            return redirect("login")
    else:
        form = UserRegistartionForm()
    context = {'form': form}
    return render(request, 'main_app/register.html', context)


def home(request):
    return render(request, 'main_app/home.html')

@login_required
def index(request):
    return render(request, 'main_app/index.html')

@login_required
def AmazonItem(request):
    if request.method == "POST":
        form = AddItemForm(request.POST)
        if form.is_valid():
            items = ItemsTracked(user=request.user, url=request.POST['url'], desired_price=request.POST['desired_price'], website = "Amazon")
            items.save()
        messages.success(request,f"Item Added from {request.user.username} Successfully!")
    else:
     form = AddItemForm()

    items = ItemsTracked.objects.filter(user=request.user, website = "Amazon")
    context = {'items':items, 'form':form}
    return render(request, 'main_app/amazon.html', context)

@login_required
def delete_item_amazon(request,pk=None):
    ItemsTracked.objects.get(id=pk).delete()
    return redirect("amazon")

@login_required
def FlipkartItem(request):
    if request.method == "POST":
        form = AddItemForm(request.POST)
        if form.is_valid():
            items = ItemsTracked(user=request.user, url=request.POST['url'], desired_price=request.POST['desired_price'], website = "Flipkart")
            items.save()
        messages.success(request,f"Item Added from {request.user.username} Successfully!")
    else:
     form = AddItemForm()

    items = ItemsTracked.objects.filter(user=request.user, website = "Flipkart")
    context = {'items':items, 'form':form}
    return render(request, 'main_app/flipkart.html', context)

@login_required
def delete_item_flipkart(request,pk=None):
    ItemsTracked.objects.get(id=pk).delete()
    return redirect("flipkart")

@login_required
def view_all(request):
     items = ItemsTracked.objects.filter(user=request.user)
     context = {'items':items}
     return render(request, 'main_app/view_all.html', context)

@login_required
def delete_item(request, pk=None):
     ItemsTracked.objects.get(id=pk).delete()
     return redirect("view-all")




def search_price():

    hdr = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Accepted-Language": "en-GB, en-US; q = 0.9, en; q = 0.8",

    }

    for item in ItemsTracked.objects.all():
        user = item.user

        if item.status == False:
            user = item.user
            user_email = user.email
            item_url = item.url
            desired_price = item.desired_price
            website = item.website
            item_name = item.name

            response = requests.get(item_url, headers=hdr)

            soup = BeautifulSoup(response.text, "lxml")

            if website == "Amazon":
               
                price = soup.select_one(selector=".a-price-whole").getText()
                price = price.replace(",", "")
                price = float(price)

            if website == "Flipkart":
            
                price = soup.select_one(selector="._30jeq3").getText()
                price = price[1:]
                price = price.replace(",", "")
                price = float(price)

            if price <= desired_price:
               subject = 'Your product has now reduced!!!'
               message = f"HI {user.username}, your product {item_name}, that you set to track has now reduced to ₹{price}. URL : {item_url}"
               email_from = settings.EMAIL_HOST_USER
               recipient_list = [user_email]
               send_mail(subject, message, email_from, recipient_list)
               item.status = True
               item.save()

        else:
            item.save()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(search_price, 'interval', minutes=60)
    scheduler.start()


