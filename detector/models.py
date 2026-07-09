import os
import uuid
from django.db import models
from django.utils import timezone


def unique_video_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    unique_id = uuid.uuid4().hex[:10]
    return f'videos/{timestamp}_{unique_id}.{ext}'


def detected_shape_path(instance, filename):
    video_id = instance.video_id or 'unknown_video'
    return f'detected_shapes/video_{video_id}/{filename}'


class VideoUpload(models.Model):
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    ]
    video = models.FileField(upload_to=unique_video_path)
    original_name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.original_name or str(self.video.name)
    

class DetectedShape(models.Model):
    video = models.ForeignKey(VideoUpload, on_delete=models.CASCADE, related_name='shapes')
    shape_name = models.CharField(max_length=50)
    snapshot = models.ImageField(upload_to=detected_shape_path)
    frame_number = models.IntegerField()
    timestamp_seconds = models.FloatField(default=0)
    confidence_note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.shape_name} from {self.video_id}'
