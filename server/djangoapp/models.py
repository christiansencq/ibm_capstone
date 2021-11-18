from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils.timezone import now

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    make = ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    dealer_id = models.CharField(max_length=40)

    type_choices = [ ('SEDAN', 'Sedan'),
                     ('SUV', 'SUV'),
                     ('WAGON', 'StationWagon'),
                     ('PICKUP', 'Pick-Up'),
                     ('MINIVAN', 'Minivan') ]
    type = models.CharField(max_length=50, 
                            choices=type_choices)
    year = models.DateField(null=True)

    def __str__(self):
        return self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, 
                    lat, long, short_name, st, state, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.state = state
        self.zip = zip

    def __str__(self):
        return self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
# Sentiment will be reviewed 


class DealerReview():
    def __init__(self, id, name, review, purchase, car_make, car_model, car_year, purchase_date):
        self.id = id
        self.name = name
        self.review = review
        self.purchase = purchase
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.purchase_date = purchase_date

    def __str__(self):
        return self.name