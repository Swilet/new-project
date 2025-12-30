from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Travel(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name