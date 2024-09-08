from django.urls import path
from .views import *

urlpatterns=[
    path("",LoginView.as_view(),name="log"),
    path("logout/",logoutView,name="lout"),
    path("register/",RegView.as_view(),name="reg"),
]