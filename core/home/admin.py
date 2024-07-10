from django.contrib import admin
from .models import Color , Person


# Register your models here.
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    class Meta:
        model = Color

    list_display = ['id', 'color_name']

    

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    class Meta:
        model = Person 

    list_display = ['id', 'name', 'age' , 'color']
    