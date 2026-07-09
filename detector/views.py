from django.shortcuts import render, redirect, get_object_or_404
from .forms import VideoUploadForm
from .models import VideoUpload
from .tasks import process_video_task


def upload_video(request):
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)

        if form.is_valid():
            video_obj = form.save(commit=False)
            video_obj.original_name = request.FILES["video"].name
            video_obj.status = "queued"
            video_obj.save()

            # Queue the background task
            process_video_task.delay(video_obj.id)

            return redirect("video_result", video_id=video_obj.id)

    else:
        form = VideoUploadForm()

    return render(request, "detector/upload.html", {"form": form})


def video_result(request, video_id):
    video = get_object_or_404(VideoUpload, id=video_id)
    return render(request, "detector/result.html", {"video": video})
