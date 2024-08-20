from django.contrib import admin
from django import forms
from django.db import models
from .models import BlogPost, ContentType, Content, Category
from django.utils.html import format_html

class ContentAdminForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = '__all__'
    
    def clean_data(self):
        data = self.cleaned_data.get('data')
        content_type = self.cleaned_data.get('content_type')
        if content_type.type == 'Paragraph':
            if not all(key in data for key in ('header', 'text')):
                raise forms.ValidationError('Paragraph must contain "header" and "text".')
        elif content_type.type == 'Point':
            if not 'points' in data:
                raise forms.ValidationError('Points must contain "points".')
        return data

    
class ContentAdmin(admin.ModelAdmin):
    form = ContentAdminForm
    list_display = ('order', 'truncated_title','truncated_data','blog_post')
    list_filter = ('content_type', 'blog_post')
    ordering = ("-blog_post",'-order')
    # ordering = ('content_type', 'blog_post')
    search_fields = ('blog_post__title','data')  # Enable search by BlogPost title, content data

    def truncated_data(self, obj):
        # Assuming data is a JSONField and you want to truncate its string representation
        data_str = str(obj.data)
        if len(data_str) > 30:
            return format_html('{}...', data_str[:100])
        return data_str

    truncated_data.short_description = 'Data (truncated)'
    
    def truncated_title(self, obj):
        # Assuming data is a JSONField and you want to truncate its string representation
        data_str = str(obj.blog_post)
        if len(data_str) > 30:
            return format_html('{}...', data_str[:30])
        return data_str

    truncated_title.short_description = 'Post title (truncated)'

    
    

admin.site.register(BlogPost)
admin.site.register(ContentType)
admin.site.register(Category)
admin.site.register(Content, ContentAdmin)
