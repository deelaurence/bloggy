from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns=[ 
    path('',  cache_page(60 *60* 24)(Home.as_view()), name="home"),
    path('posts/', cache_page(60 *60* 24)(BlogList.as_view()), name="posts"),
    path('add/',  ContentCreateView.as_view(), name="content_create"),
    path('posts/category/<slug:category_slug>',cache_page(60 *60* 24)(BlogList.as_view()), name="posts_category"),
    path('post/<str:title>/', cache_page(60 *60* 24)(BlogPostDetailView.as_view()), name="post")
]
# urlpatterns=[ 
#     path('',  Home.as_view(), name="home"),
#     path('posts/', BlogList.as_view(), name="posts"),
#     path('add/',  ContentCreateView.as_view(), name="content_create"),
#     path('posts/category/<slug:category_slug>',BlogList.as_view(), name="posts_category"),
#     path('post/<str:title>/',BlogPostDetailView.as_view(), name="post")
# ]