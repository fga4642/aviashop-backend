from django.contrib import admin

from spares.models import *

admin.site.register(Spare)
admin.site.register(Order)
admin.site.register(CustomUser)