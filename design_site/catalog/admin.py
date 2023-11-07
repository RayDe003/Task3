from django.contrib import admin

from .models import CustomUser, DesignCategory, Request

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(DesignCategory)
admin.site.register(Request)