from django.db import models
from django_quill.fields import QuillField


def blog_image_directory_path(instance: "Blog", filename: str) -> str:
    return "blog_images/blog_{pk}__{filename}".format(
        pk=instance.pk,
        filename=filename
    )


class Blog(models.Model):
    preview_image = models.ImageField(upload_to=blog_image_directory_path)
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Bloglar'
        

class News(models.Model):
    preview_image = models.ImageField(upload_to=blog_image_directory_path)
    title = models.CharField(max_length=500)
    description = QuillField(null=True, blank=True)
    text = QuillField(null=True, blank=True)
    popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'