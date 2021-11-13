from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
#from .restapis import post_request
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
        # else:
        #     context['alert'] = "Invalid Login"
        #     return render(request, 'djangoapp/index.html', context)
    
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
    # if request.method == "GET":
    #     return render(request, 'djangoapp/index.html', context)

    if request.method == "GET":
        url = ""
        # url = os.getenv("API_DEALERSHIP_URL")
        # Get dealers from the URL

        # dealerships = get_dealers_from_cf(url)
        
        #context={"dealership_list":dealerships}
        
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html')

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):

    if request.method == "GET":
        url = ""
        # url = os.getenv("API_REVIEW_URL")
        # reviews = get_dealer_reviews_from_cf(url, dealerid=dealer_id)
        # context = {"review_list":reviews, "dealer_id":dealer_id}
        return render(request, 'djangoapp/dealer_details.html')


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "GET":
        context = {}
        cars = list(CarModel.objects.filter(dealer_id=dealer_id))
        context["cars"] = cars
        context["dealer_id"] = dealer_id
        return render(request, "djangoapp/add_review.html", context)

    if request.method == "POST":
        url = ""
        if request.user.is_authenticated:
            car = CarModel.objects.get(id=request.POST["car"])
            review = {}
            review["dealership"] = dealer_id
            review["review_content"] = request.POST["content"]
            review["time"] = datetime.utcnow().isoformat()
            review["car_model"] = car.model
            review["car_make"] = car.make            
            
            json_payload = {}
            json_payload["review"] = review

            post_request(url, json_payload, dealerID=dealer_id)

            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)