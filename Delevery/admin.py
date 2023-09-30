from django.contrib import admin
from .models import Order, BaseModel

# Register your models here.
admin.site.register(Order)
admin.site.register(BaseModel)
