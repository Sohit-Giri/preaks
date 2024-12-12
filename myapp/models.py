from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

class Forum(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)
    photo = models.FileField(upload_to='myapp-image')
    post = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title