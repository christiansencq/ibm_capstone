from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import post_request, get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id
# get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import os


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == 'POST':
        #Get the username and password variables.
        username = request.POST['username']
        password = request.POST['password']
        #Check the username/password match and authenticate
        user = authenticate(username=username, password=password)
        if user is not None:
            #If user is valid, call login method.
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['alert'] = "Invalid Login"
            return render(request, 'djangoapp/index.html', context)
    
    #If its a GET request, just show the page.
#    return render(request, 'djangoapp/index.html', context)
    return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')
       

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        #Pulling up the registration page.
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        #Submitting a registration request submission.
            #Check for valid username(i.e. not already taken)
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        password = request.POST['password']
        user_already_exists = False
        try:
            User.objects.get(username=username)
            user_already_exists = True
        except:
            logger.debug("{} is new user".format(username))

        if not user_already_exists:
            #Create user in auth_user table
            #User.objects is the UserManager, which can create_user 
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            user.save()
            login(request, user)
            #User successfully created, redirect to main page.
            return redirect("djangoapp:index")
        else:
            context['alert'] = "User exists."
            #Try again.
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):

    if request.method == "GET":
        context=dict()
        url = "https://6b6023fb.us-south.apigw.appdomain.cloud/api/dealership"
        
        # Get dealers from the URL

        dealerships, result = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        context["result"] = result
        
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):

    if request.method == "GET":
        context=dict()
        url = "https://6b6023fb.us-south.apigw.appdomain.cloud"
        dealer_url = url + "/api/dealership"
        review_url = url + "/api/review"

        dealer, dealer_status = get_dealer_by_id(dealer_url, dealer_id)
        context["dealer"] = dealer
        context["dealer_result"] = dealer_status

        reviews, review_status = get_dealer_reviews_from_cf(review_url, dealer_id)
        context["reviews"]=reviews
        context["review_result"]=review_status

        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "GET":
        context = dict()
        url = "https://6b6023fb.us-south.apigw.appdomain.cloud/api/dealership"

        dealer, dealer_status = get_dealer_by_id(url, dealer_id)
        context["dealer"] = dealer
        context["result"] = dealer_status
        cars = CarModel.objects.all().filter(dealer_id=dealer_id)
        context["cars"] = cars

        return render(request, "djangoapp/add_review.html", context)

    elif request.method == "POST":
        if request.user.is_authenticated:
            url = "https://6b6023fb.us-south.apigw.appdomain.cloud/api/review"
            review = dict()
            review["name"] = request.user.username
            review["dealership"] = dealer_id
            review["review"] = request.POST["content"]
            review["purchase"] = True if (request.POST.get('purchasecheck', "False") == "on") else False
            car_id = request.POST.get("car", None)
            if car_id != None:
                car = CarModel.objects.get(id=car_id)
                review["car_make"] = car.car_make.name
                review["car_model"] = car.name
                review["car_year"] = int(car.yearpublished())
                review["purchase_date"] = request.POST["purchasedate"]
                     
            json_payload = dict()
            json_payload["review"] = review
            result, status_code = post_request(url, json_payload, dealerId = dealer_id)
            print(result)

            if (result["ok"]):
                return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
            else:
                context=dict()
                context["error"] = result["message"]
                return render(request, 'djangoapp/add_review.html', context)
        else:    
            context=dict()
            context["error"] = "User is not authenticated"
            url = "https://6b6023fb.us-south.apigw.appdomain.cloud/api/dealership"
            dealer, dealer_status = get_dealer_by_id(url, dealer_id)
            context["dealer"] = dealer
            context["result"] = dealer_status
            cars = CarModel.objects.all().filter(dealer_id = dealer_id)
            
            return render(request, "djangoapp/add_review.html", context)