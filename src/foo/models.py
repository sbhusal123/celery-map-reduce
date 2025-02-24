from django.db import models
from django.core.validators import FileExtensionValidator

class Document(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(
        upload_to='pdfs/', 
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    pdf_text = models.TextField(blank=True)

    def __str__(self):
        return self.title
