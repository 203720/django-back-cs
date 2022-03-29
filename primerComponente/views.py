from multiprocessing import context
from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from primerComponente.models import PrimerTabla
from primerComponente.serializers import PrimerTablaSerializer
class PrimerTablaList(APIView):
    def response_custom(self,message, pay_load, status):
        response_x = {"messages":message, "pay_load":pay_load, "status":status}
        response_y = json.dumps(response_x)
        response_ok = json.loads(response_y)
        return response_ok

    def get(self, request, format=None):
        queryset=PrimerTabla.objects.all()
        serializer=PrimerTablaSerializer(queryset,many=True ,context={'request':request})
        response_ok = self.response_custom("Success", serializer.data, status.HTTP_200_OK)
        return Response(response_ok)

    def post(self, request, format=None):
        serializer = PrimerTablaSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            datas = serializer.data
            return Response(datas,  status.HTTP_201_CREATED)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

class PrimerTablaDetail(APIView):
    def get_object(self, pk):
        try:
            return PrimerTabla.objects.get(pk = pk)
        except PrimerTabla.DoesNotExist:
            return 0

    def get(self, request, pk, format=None):
        id_response = self.get_object(pk)
        if id_response != 0:
            id_response = PrimerTablaSerializer(id_response)
            return Response(id_response.data, status = status.HTTP_200_OK)
        return Response("No hay datos",status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        id_response = self.get_object(pk)
        serializer = PrimerTablaSerializer(id_response, data = request.data)
        if serializer.is_valid():
            serializer.save()
            datas = serializer.data
            return Response(datas,status =status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        objetive = self.get_object(pk)
        if objetive!="No existe":
            objetive.delete()
            return Response("Dato eliminado",  status = status.HTTP_200_OK)
        else:
            return Response("Dato no encontrado", status = status.HTTP_400_BAD_REQUEST)