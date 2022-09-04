from rest_framework_gis import serializers as gserializers
from .models import Marker
from rest_framework import serializers

class MarkerSerializer(gserializers.GeoFeatureModelListSerializer):
    class Meta:
        model = Marker
        fields = ("id","name")
        geo_field = "location"


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = ('image',)
