from django.db import models


class Category(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    cover_image = models.CharField(max_length=500)
    summary = models.CharField(max_length=500)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ContentType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class Content(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    order = models.IntegerField()
    data = models.JSONField()

    class Meta:
        unique_together = ('blog_post', 'order')
        ordering = ["-blog_post",'-order']  # Default ordering

    def __str__(self):
        return f'{self.content_type} for {self.blog_post} at order {self.order}'
