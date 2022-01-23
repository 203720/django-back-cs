from django.urls import path, re_path
from django.conf.urls import include

#Importacion de vistas
from register.views import UserRegister

urlpatterns = [
    re_path(r'^', UserRegister.as_view()),
] 