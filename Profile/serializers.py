from rest_framework import serializers
from Profile.models import ProfileTable
class ProfileTablaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileTable
        fields = ('__all__')