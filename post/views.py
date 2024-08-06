from typing import Any
from django.views.generic.detail import DetailView 
from django.views.generic import ListView
from .models import BlogPost, Content, Category
from django.shortcuts import get_object_or_404


class Home(ListView):
    model = BlogPost
    template_name = './index.html'
    context_object_name='posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['contents'] = Content.objects.all()        
        return context

class BlogList(ListView):
    model = BlogPost
    template_name = './all_posts.html'
    context_object_name='posts'

    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug') 
        if category_slug:
            queryset = queryset.filter(category=category_slug)
        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = 'All Posts'
        if self.kwargs.get('category_slug'): 
            category=Category.objects.get(id=self.kwargs.get('category_slug'))
            context['current_category'] = category
        return context


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = './blog.html'
    context_object_name = 'blog_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contents'] = Content.objects.filter(blog_post=self.object).order_by('order')
        return context




