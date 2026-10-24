
from django.contrib import admin
from .models import Prescription,Patient

admin.site.register(Prescription)
admin.site.register(Patient)