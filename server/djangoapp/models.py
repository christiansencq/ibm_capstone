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
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class CarModel(models.Model):
    make = ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    dealer_id = models.IntegerField()

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

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, name, city, zipcode):
        self.name = name
        self.city = city
        self.zipcode = zipcode

    def __str__(self):
        return self.name

# <HINT> Create a plain Python class `DealerReview` to hold review data
# Sentiment will be reviewed 
class DealerReview():
    def __init__(self, dealer_name, author, review_content, car_make, car_model):
        self.dealer_name = dealer_name
        self.author = author
        self.review_content = review_content
        self.car_make = car_make
        self.car_model = car_model

    def __str__(self):
        return self.name
