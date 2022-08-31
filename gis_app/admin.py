from django.contrib.gis import admin
from .models import Marker, Profile
from django.contrib.auth import get_user_model


User = get_user_model()
# Register your models here.

@admin.register(Marker)
class MakerAdmin(admin.OSMGeoAdmin):
    list_display = ("name", "id", "date")


    
@admin.register(Profile)
class MakerAdmin(admin.OSMGeoAdmin):
    list_display = ("username", "title", "home")

    def username(self, obj):
        return obj.user.username