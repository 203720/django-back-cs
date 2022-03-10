from rest_framework import serializers
#Importancion de modelos
from Profile.models import ProfileTable

class ProfileTablaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProfileTable
        fields = ('__all__')