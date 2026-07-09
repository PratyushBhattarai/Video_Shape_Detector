import subprocess
from pathlib import Path


def extract_frames(video_path, output_dir, fps=1):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_pattern = str(output_dir / "frame_%06d.jpg")

    command = [
        "ffmpeg",
        "-y",
        "-i", str(video_path),
        "-vf", f"fps={fps}",
        output_pattern,
    ]

    subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )

    return sorted(output_dir.glob("frame_*.jpg"))