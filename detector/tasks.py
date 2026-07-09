import shutil
import tempfile
from pathlib import Path

import cv2
from celery import shared_task
from django.core.files.base import ContentFile
from django.utils import timezone

from .models import VideoUpload, DetectedShape
from .shape_utils import detect_shapes_in_frame
from .video_utils import extract_frames


@shared_task(bind=True)
def process_video_task(self, video_id):
    video = VideoUpload.objects.get(id=video_id)

    video.status = "processing"
    video.error_message = ""
    video.save(update_fields=["status", "error_message"])

    temp_dir = Path(tempfile.mkdtemp(prefix=f"video_{video_id}_"))

    try:
        video_path = video.video.path
        frames_dir = temp_dir / "frames"

        frame_paths = extract_frames(video_path, frames_dir, fps=1)

        for index, frame_path in enumerate(frame_paths, start=1):
            detected_items = detect_shapes_in_frame(frame_path)

            for item_index, item in enumerate(detected_items, start=1):
                success, encoded_image = cv2.imencode(".jpg", item["crop"])

                if not success:
                    continue

                filename = f"frame_{index:06d}_shape_{item_index}.jpg"

                shape = DetectedShape(
                    video=video,
                    shape_name=item["shape_name"],
                    frame_number=index,
                    timestamp_seconds=float(index - 1),
                    confidence_note=item["note"],
                )

                shape.snapshot.save(
                    filename,
                    ContentFile(encoded_image.tobytes()),
                    save=True,
                )

        video.status = "done"
        video.processed_at = timezone.now()
        video.save(update_fields=["status", "processed_at"])

    except Exception as exc:
        video.status = "failed"
        video.error_message = str(exc)
        video.save(update_fields=["status", "error_message"])
        raise

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)