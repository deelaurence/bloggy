from django.urls import path
from .views import *


urlpatterns=[
    path('',  Home.as_view(), name="home"),
    path('posts/',  BlogList.as_view(), name="posts"),
    path('posts/category/<slug:category_slug>',  BlogList.as_view(), name="posts_category"),
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name="post")
]