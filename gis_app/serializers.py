from rest_framework_gis import serializers
from .models import Marker


class MarkerSerializer(serializers.GeoFeatureModelListSerializer):
    class Meta:
        model = Marker
        fields = ("id","name")
        geo_field = "location"