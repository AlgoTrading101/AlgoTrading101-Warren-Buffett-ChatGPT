"""YouTube related functions."""

import contextlib
import os
import wave

import yt_dlp

VIDEO_FORMAT = os.environ.get("VIDEO_FORMAT", "mp4")


def get_video_duration(video_path: str) -> float:
    """Get the duration of a video."""
    with contextlib.closing(wave.open(video_path, "r")) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)

    return duration


def prepare_video(video_path: str) -> tuple[str, float]:
    """Convert video to audio and return the audio file and its duration."""
    _, file_ending = os.path.splitext(f"{video_path}")
    audio_file = video_path.replace(file_ending, ".wav")
    os.system(f'ffmpeg -i "{video_path}" -ar 16000 -ac 1 -c:a pcm_s16le "{audio_file}"')

    duration = get_video_duration(audio_file)

    return audio_file, duration


def get_youtube_video(video_url: str) -> str:
    """Download a YouTube video."""
    if VIDEO_FORMAT == "m4a":
        ydl_opts = {
            "format": "bestaudio[ext=m4a]/best[ext=mp4]/best",
        }
    elif VIDEO_FORMAT == "mp4":
        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        }
    else:
        raise ValueError(f"Currenly only m4a and mp4 are supported. Got {VIDEO_FORMAT}")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        video = ydl.prepare_filename(info)
        ydl.process_info(info)

    return video


def get_video_name() -> str:
    """Get the name of the video."""
    try:
        video_name = (
            max(
                [f for f in os.listdir() if f.endswith(f".{VIDEO_FORMAT}")],
                key=os.path.getctime,
            ).split(f".{VIDEO_FORMAT}")[0]
        ).lower()
        video_name = (
            video_name.replace(":", "")
            .replace("-", "")
            .replace('"', "")
            .replace("'", "")
            .replace(" ", "_")
        )
        video_name = video_name[:80]
    except ValueError:
        video_name = "video"
    return video_name
