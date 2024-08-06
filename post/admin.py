from django.contrib import admin
from django import forms
from .models import BlogPost, ContentType, Content, Category

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
    list_display = ('content_type', 'blog_post', 'order')
    list_filter = ('content_type', 'blog_post')
    ordering = ('content_type', 'blog_post')
    search_fields = ('blog_post__title',)  # Enable search by BlogPost title

admin.site.register(BlogPost)
admin.site.register(ContentType)
admin.site.register(Category)
admin.site.register(Content, ContentAdmin)
