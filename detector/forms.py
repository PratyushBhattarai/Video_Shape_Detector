from django import forms
from .models import VideoUpload


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoUpload
        fields = ['video']

    def clean_video(self):
        video = self.cleaned_data['video']

        allowed_extensions = ['mp4', 'mov', 'avi', 'mkv']
        ext = video.name.split('.')[-1].lower()

        if ext not in allowed_extensions:
            raise forms.ValidationError(
                "Please upload MP4, MOV, AVI, or MKV videos only."
            )

        return video