from django.urls import path, re_path
from django.conf.urls import include

#Importacion de vistas
from login.views import LoginAuth, MyObtainTokenPairView

from rest_framework_simplejwt.views import TokenRefreshView
  

urlpatterns = [
    re_path(r'^v1/login', LoginAuth.as_view()),
    re_path(r'^v2/login', MyObtainTokenPairView.as_view()),
    re_path(r'^v1/refresh', TokenRefreshView.as_view()),  
] 