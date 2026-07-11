from django.contrib import admin
from .models import VideoUpload, DetectedShape

@admin.register(VideoUpload)
class VideoUploadAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "original_name",
        "status",
        "created_at",
        "processed_at",
    )
    list_filter = ("status",)
    search_fields = ("original_name",)


@admin.register(DetectedShape)
class DetectedShapeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "shape_name",
        "video",
        "frame_number",
        "timestamp_seconds",
    )
    list_filter = ("shape_name",)
