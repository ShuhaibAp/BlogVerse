from django.urls import path
from .views import *

urlpatterns=[
    path('',HomePage.as_view(),name='home'),
    path('search/',blog_search,name='blog_search'),
    path('Badd/',NewBlog.as_view(),name='badd'),
    path('bdet/<int:id>',BlogDetail.as_view(),name='bdet'),
    path('Blist/<str:cat>',BlogList.as_view(),name='blist'),
    path('Bupd/<int:id>',BlogUpdate.as_view(),name='bupd'),
    path('Bdel/<int:id>',BlogDelete,name='bdel'),
    path('blikes/<int:blog_id>',BlogLikes,name='blike'),
    path('likelist/<int:id>',LikedList.as_view(),name='likelist'),
    path('Bbookmark/<int:blog_id>',BlogBookmark,name='bookmark'),
    path('Bbooklist/<int:id>',BookmarkList.as_view(),name='booklist'),
    path('brevadd/<int:id>',AddReview,name='revadd'),
    path('revall/<int:id>',ReviewList.as_view(),name='allrev'),
    path('revedit/<int:review_id>',ReviewEdit,name='editrev'),
    path('revdel/<int:review_id>',ReviewDelete,name='revdel'),
#Profile section
    path('Padd/',NewProfile.as_view(),name='padd'),
    path('Pview/<str:user>',ProfileView.as_view(),name='pview'),
    path('Pupd/<str:user>',UpdateProfile.as_view(),name='pupd'),
    path('Pdel/<str:user>',DeleteProfile,name='pdel'),
    path('Pfollow/<int:profile_id>',FollowProfile,name='pfoll'),

    path('about',AboutView.as_view(),name='abt'),
    path('contact',ContactView.as_view(),name='cont'),
]