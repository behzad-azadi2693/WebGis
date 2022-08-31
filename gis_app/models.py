from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    home = models.PointField()
    worker = models.PointField()
    city = models.PolygonField()

    def __str__(self):
        return f'{self.user.username}-{self.id}'

    @property
    def city_point_list(self):
        return [[point.x, point.y] for point in self.city]


class Marker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    location = models.PointField()

    def __str__(self):
        return self.name


class MarkerImage(models.Model):
    msrker = models.ForeignKey(Marker, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'marker/')