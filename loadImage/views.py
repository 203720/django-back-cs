import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
import os.path
import json

from loadImage.models import PrimerTabla
from loadImage.serializers import PrimerTablaSerializer
class LoadImageTableList(APIView):
    def response_custom(self,message, pay_load, status):
        response_x = {"messages":message, "pay_load":pay_load, "status":status}
        response_y = json.dumps(response_x)
        response_ok = json.loads(response_y)
        return response_ok
        
    def get(self, request, format=None):
        queryset = PrimerTabla.objects.all()
        serializer = PrimerTablaSerializer(queryset, many = True, context = {'request':request})
        response_ok = self.response_custom("Success", serializer.data, status.HTTP_200_OK)
        return Response(response_ok)

    def post(self, request):
        if 'url_img' not in request.data:
            raise exceptions.ParseError(
                "No hay ninguna imagen")
        image = request.data['url_img']
        name, formato_img = os.path.splitext(image.name)
        request.data['name_img'] = name
        request.data['format_img'] = formato_img
        serializer = PrimerTablaSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            img = PrimerTabla(**validated_data)
            img.save()
            serializer_response = PrimerTablaSerializer(img)
            return Response(serializer_response.data,  status.HTTP_201_CREATED)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


class LoadImageTableDetail(APIView):
    def get_object(self, pk):
        try:
            return PrimerTabla.objects.get(pk = pk)
        except PrimerTabla.DoesNotExist:
            return 0

    def get(self, request,pk, format=None):
        id_response = self.get_object(pk)
        if id_response != 0:
            id_response = PrimerTablaSerializer(id_response)
            return Response(id_response.data, status = status.HTTP_200_OK)
        return Response("No hay imagenes", status = status.HTTP_400_BAD_REQUEST)


    def put(self, request,pk, format=None):
        id_response = self.get_object(pk)
        image = request.data['url_img']
        name, formato_img = os.path.splitext(image.name)
        request.data['name_img'] = name
        request.data['format_img'] = formato_img
        serializer = PrimerTablaSerializer(data=request.data)
        request.data['edited'] = datetime.datetime.now()
        serializer = PrimerTablaSerializer(id_response, data = request.data)
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


