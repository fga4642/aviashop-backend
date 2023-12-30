from django.contrib import admin

# Register your models here.
from spares.models import *

admin.site.register(Spare)
admin.site.register(Order)