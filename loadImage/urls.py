from django.urls import path, re_path
from django.conf.urls import include

#Importacion de vistas
from loadImage.views import LoadImageTableList
from loadImage.views import LoadImageTableDetail

urlpatterns = [
    re_path(r'^lista/$', LoadImageTableList.as_view()),
    re_path(r'^lista/(?P<pk>\d+)$', LoadImageTableDetail.as_view()),    
]