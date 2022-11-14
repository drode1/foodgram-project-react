from django.contrib import admin

# Register your models here.
from recipes.models import Tag, Ingredient

admin.site.register(Tag)
admin.site.register(Ingredient)
