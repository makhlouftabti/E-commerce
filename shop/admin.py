from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Brand)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Cart)

