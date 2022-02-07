# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
import os.path

#Importación de modelos
from loadImage.models import PrimerTabla

from loadImage.serializers import PrimerTablaSerializer

class LoadImageTableList(APIView):
    def get(self, request, format=None):
        queryset = PrimerTabla.objects.all()
        serializer = PrimerTablaSerializer(queryset, many = True, context = {'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if 'url_img' not in request.data:
            raise exceptions.ParseError(
                "No hay ninguna imagen")
        image = request.data['url_img']
        serializer = PrimerTablaSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            img = PrimerTabla(**validated_data)
            img.save()
            serializer_response = PrimerTablaSerializer(img)
            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoadImageTableDetail(APIView):
    def get_object(self, pk):
        try:
            return PrimerTabla.objects.get(pk = pk)
        except PrimerTabla.DoesNotExist:
            return 0

    def get(self, request,pk, format=None):
        idResponse = self.get_object(pk)
        if idResponse != 0:
            idResponse = PrimerTablaSerializer(idResponse)
            return Response(idResponse.data, status = status.HTTP_200_OK)
        return Response("No hay imagenes", status = status.HTTP_400_BAD_REQUEST)


    def put(self, request,pk, format=None):
        idResponse = self.get_object(pk)
        image = request.data['url_img']
        serializer = PrimerTablaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            datas = serializer.data
            return Response(datas, status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        img = self.get_object(pk)
        if img != 0:
            img.url_img.delete(save=True)
            img.delete()
            return Response("Imagen eliminada",status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Imagen no encontrada",status = status.HTTP_400_BAD_REQUEST)