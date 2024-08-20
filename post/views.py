from typing import Any
from django.views.generic.detail import DetailView 
from django.views.generic import ListView
from .models import BlogPost, Content, Category,ContentType
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError
import json

def space_to_dash(text):
    return text.replace(' ','-')
def dash_to_space(text):
    return text.replace('-',' ')



class ContentCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Extracting data from the request body (assuming JSON format)
            print(request)
            data = json.loads(request.body.decode('utf-8'))
            blog_post_id = data.get('blog_post_id')
            content_data = data.get('content')  # This should be an array of dictionaries

            if not blog_post_id or not content_data:
                return JsonResponse({'error': 'Missing blog_post_id or content data'}, status=400)

            # Get the BlogPost instance
            blog_post = get_object_or_404(BlogPost, id=blog_post_id)

            for index, item in enumerate(content_data):
                content_type_id = item.get('content_type_id')
                content_data_item = item.get('data')

                if not content_type_id or not content_data_item:
                    continue  # Skip this entry if any required data is missing

                # Get the ContentType instance
                content_type = get_object_or_404(ContentType, id=content_type_id)

                # Create and save Content instance
                content_instance = Content.objects.create(
                    content_type=content_type,
                    blog_post=blog_post,
                    order=index + 1,  # Order based on position in the array
                    data=content_data_item
                )
                content_instance.save()

            return JsonResponse({'message': 'Content created successfully'}, status=201)

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'An error occurred while saving content'}, status=500)


    def delete(self,request):
        try:
            # Extracting data from the request body (assuming JSON format)
            print(request)
            data = json.loads(request.body.decode('utf-8'))
            blog_post_id = data.get('blog_post_id')
            
            if not blog_post_id: 
                return JsonResponse({'error': 'Missing blog_post_id'}, status=400)

            # Get the BlogPost instance
            blog_post = get_object_or_404(BlogPost, id=blog_post_id)

            contents= Content.objects.filter(blog_post=blog_post).delete()
            print(contents)
            return JsonResponse({'message': 'Content removed',"contents":contents}, status=201)

        except ValidationError as e:
                return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
                print(e)
                return JsonResponse({'error': 'An error occurred while saving content'}, status=500)



# get data for homepage
class Home(ListView):
    model = BlogPost
    template_name = './index.html'
    context_object_name='posts'

    def get_context_data(self, **kwargs):    
        context = super().get_context_data(**kwargs)
        
        # so that the url has a dash instead of %20
        posts_with_dash_in_title=[]

        for post in context['posts']:
            post.dash_title=space_to_dash(post.title)
            posts_with_dash_in_title.append(post)

        context['posts']=posts_with_dash_in_title
        return context



# get by category or list all
class BlogList(ListView):
    model = BlogPost
    template_name = './all_posts.html'
    context_object_name='posts'

    # return a list of blog posts the query will display
    def get_queryset(self):
        # get list of blog post
        queryset = super().get_queryset()
        # category_slug could be present in the url params
        category_slug = self.kwargs.get('category_slug') 
        # filter queryset according to the category
        if category_slug:
            queryset = queryset.filter(category=category_slug)
        return queryset
    
    # build the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # add key called categories to context
        context['categories'] = Category.objects.all()
        context['current_category'] = 'All Posts'
        if self.kwargs.get('category_slug'): 
            category=Category.objects.get(id=self.kwargs.get('category_slug'))
            context['current_category'] = category
        
        posts_with_dash_in_title=[]
    
        for post in context['posts']:
            post.dash_title=space_to_dash(post.title)
            posts_with_dash_in_title.append(post)

        context['posts']=posts_with_dash_in_title
        return context
        
        
        

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = './blog.html'
    context_object_name = 'blog_post'

    def get_object(self, queryset=None):
        title = self.kwargs.get('title')
        return get_object_or_404(BlogPost, title=dash_to_space(title))

    def get_context_data(self, **kwargs):
        print(self.object)
        context = super().get_context_data(**kwargs)
        context['contents'] = Content.objects.filter(blog_post=self.object).order_by('order')
        return context




