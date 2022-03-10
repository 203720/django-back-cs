from django.urls import re_path
#Importacion de vistas
from Profile.views import ProfileTableList, ProfileTableDetail, ProfileTableUsersDetail


urlpatterns = [
    re_path(r'^new_profile', ProfileTableList.as_view()),
    re_path(r'^user/(?P<pk>\d+)/$',ProfileTableDetail.as_view()),
    re_path(r'^update_user/(?P<pk>\d+)/$',ProfileTableUsersDetail.as_view()),
] 