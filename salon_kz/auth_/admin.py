from django.contrib import admin
from main import models


admin.site.register(models.CustomUser)
admin.site.register(models.Country)
admin.site.register(models.City)
admin.site.register(models.Client)
admin.site.register(models.Partner)
admin.site.register(models.Salon)
admin.site.register(models.Service)
admin.site.register(models.Master)
admin.site.register(models.MasterService)
admin.site.register(models.Order)
admin.site.register(models.Comment)
admin.site.register(models.Rating)
