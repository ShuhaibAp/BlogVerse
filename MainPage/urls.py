from django.urls import path
from .views import *

urlpatterns=[
    path('',HomePage.as_view(),name='home'),
    path('Badd/',NewBlog.as_view(),name='badd'),
    path('bdet/<int:id>',BlogDetail.as_view(),name='bdet'),
    path('Blist/<str:cat>',BlogList.as_view(),name='blist'),

    path('Padd/',NewProfile.as_view(),name='padd'),
    path('Pview/<str:user>',ProfileView.as_view(),name='pview'),
    path('Pupd/<str:user>',UpdateProfile.as_view(),name='pupd'),
    path('Pdel/<str:user>',DeleteProfile,name='pdel'),
]