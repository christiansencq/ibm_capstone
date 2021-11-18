from django.contrib import admin
from .models import CarModel, CarMake


# Register your models here.



# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('car_make', 'name', 'type', 'dealer_id')
    fields = ['name', 'car_make', 'type', 'dealer_id']
    search_fields = ['name']
    inlines = [CarModelInline]

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]


# Register models here
admin.site.register(CarModel)
admin.site.register(CarMake)