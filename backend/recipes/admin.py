from django.contrib import admin

# Register your models here.
from recipes.models import Tag

admin.site.register(Tag)
