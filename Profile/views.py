from ast import If
import json
from urllib import response
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
import os
import datetime
from Profile.models import ProfileTable
from django.contrib.auth.models import User
from Profile.serializers import ProfileTablaSerializer
class ProfileTableList(APIView):

    def get_objectUser(self, id_user):
        try:
            return User.objects.get(pk = id_user)
        except User.DoesNotExist:
            return 0
    
        
    def post(self, request):
        if 'url_img' not in request.data:
            raise exceptions.ParseError(
                "No se ha seleccionado una imagen")
        id_user = request.data['id_user']
        user = self.get_objectUser(id_user)
        if(user!=0):
            serializer = ProfileTablaSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                profile = ProfileTable(**validated_data)
                profile.save()
                serializer_response = ProfileTablaSerializer(profile)
                return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response("Error", status=status.HTTP_400_BAD_REQUEST)
    
class ProfileTableDetail(APIView):

    def get_object(self, pk):
        try:
            return ProfileTable.objects.get(id_user = pk)
        except ProfileTable.DoesNotExist:
            return 0
    
    def get(self, request, pk, format=None):
        id_response = self.get_object(pk)
        if id_response != 0:
            id_response = ProfileTablaSerializer(id_response)
            return Response(id_response.data, status = status.HTTP_200_OK)
        return Response("No hay datos", status = status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        archivos = request.data['url_img']
        id_response = self.get_object(pk)
        if(id_response != 0):
            try:
                os.remove('assets/'+str(id_response.url_img))
            except os.error:
                print("La imagen no se encontro")
            id_response.url_img = archivos
            id_response.save()
            return Response("Imagen actualizada", status=status.HTTP_201_CREATED)
        else:
            return Response("Error")
    
    def delete(self, request, pk):
        profile = self.get_object(pk)
        if profile != 404:
            profile.url_img.delete(save=True)
            return Response("Imagen eliminada",status=status.HTTP_204_NO_CONTENT)
        return Response("La imagen no se encontro",status = status.HTTP_400_BAD_REQUEST)

class ProfileTableUsersDetail(APIView):

    def get(self, request, pk, format=None):
        id_response = User.objects.filter(id=pk).values()
        if(id_response != 0):
            response_data = self.res_custom(id_response, status.HTTP_200_OK)
            return Response(response_data)
        return("User no encontrado")

    def put(self, request, pk, format=None):
        data = request.data
        user = User.objects.filter(id = pk)
        user.update(username = data.get('username'))
        user.update(first_name = data.get('first_name'))
        user.update(last_name = data.get('last_name'))
        user.update(email = data.get('email'))
        user_update = User.objects.filter(id=pk).values()
        return Response(self.res_custom(user_update, status.HTTP_200_OK))

    def res_custom(self, user, status):
        json_response = {
            "first_name" : user[0]['first_name'],
            "last_name" : user[0]['last_name'],
            "username" : user[0]['username'],
            "email" : user[0]['email'],
            "status" : status
        }
        return json_response