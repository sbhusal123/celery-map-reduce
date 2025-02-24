from django.db import models
from django.core.validators import FileExtensionValidator

from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import process_pdf_task

class Document(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(
        upload_to='pdfs/', 
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    pdf_text = models.TextField(blank=True)
    entities = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        m =  super().save(*args, **kwargs)
        return m



@receiver(post_save, sender=Document)
def trigger_send_email_task(sender, instance, created, **kwargs):
    if created:
        process_pdf_task.delay(instance.id)

post_save.connect(trigger_send_email_task, sender=Document)
