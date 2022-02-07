from rest_framework import serializers

#Importancion de modelos
from loadImage.models import PrimerTabla

class PrimerTablaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimerTabla
        fields = ('__all__')