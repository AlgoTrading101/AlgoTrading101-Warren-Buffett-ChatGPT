"""Transcribe and perform diarization on a YouTube video using OpenAI Whisper."""

import os
import time
from typing import Generator

import numpy as np
import pandas as pd
import stable_whisper
import torch
from gradio.components.video import Video
from pyannote.audio import Audio
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.core import Segment

from diarization import find_n_speakers, label_segments_with_speakers
from helpers import get_sytem_info, prepare_output
from youtube import get_video_name, prepare_video

huggingface_token = os.environ.get("HUGGINGFACE_TOKEN")

embedding_model = PretrainedSpeakerEmbedding(
    "speechbrain/spkrec-ecapa-voxceleb",
    device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
    use_auth_token="huggingface_token",
)

VIDEO_FORMAT = os.environ.get("VIDEO_FORMAT", "mp4")


def create_segments(segments_raw):
    """Create segments from the raw segments."""
    segments = []

    for segment_chunk in segments_raw:
        chunk = {}
        chunk["start"] = segment_chunk.start
        chunk["end"] = segment_chunk.end
        chunk["text"] = segment_chunk.text
        segments.append(chunk)

    return segments


def segment_embedding(segment, duration: float, audio_file: str):
    """Create an embedding for a segment."""
    audio = Audio()
    start = segment["start"]
    end = min(duration, segment["end"])

    clip = Segment(start, end)
    waveform, _ = audio.crop(audio_file, clip)
    return embedding_model(waveform[None])


def create_embeddings_and_segments(
    segments_raw: Generator, duration: float, audio_file: str
):
    """Create embeddings and segments from the raw segments."""
    segments = create_segments(segments_raw)
    embeddings = np.zeros(shape=(len(segments), 192))
    for i, segment in enumerate(segments):
        embeddings[i] = segment_embedding(segment, duration, audio_file)
    embeddings = np.nan_to_num(embeddings)

    return embeddings, segments


def transcription_and_diarization(
    video_file: Video,
    whisper_model: str,
    num_speakers: int,
) -> list:
    """Transcribe and diarization execution."""
    model = stable_whisper.load_model(whisper_model)

    audio_file, duration = prepare_video(video_file)

    result = model.transcribe(audio_file)
    segments_raw = result.segments

    # Clear up the memory
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    embeddings, segments = create_embeddings_and_segments(
        segments_raw, duration, audio_file
    )

    if num_speakers == 0:
        final_num_speakers = find_n_speakers(embeddings)
    else:
        final_num_speakers = num_speakers

    segments = label_segments_with_speakers(final_num_speakers, embeddings, segments)

    return segments


def speech_to_text(
    video_file: Video,
    whisper_model: str,
    num_speakers: int,
):
    """Transcribe and perform diarization on a YouTube video using OpenAI Whisper.

    Speech Recognition is based on models from OpenAI Whisper https://github.com/openai/whisper
    Speaker diarization is done by an ensemble of models.
    """
    time_start = time.time()

    segments = transcription_and_diarization(video_file, whisper_model, num_speakers)
    result_dict = prepare_output(segments)

    time_end = time.time()
    time_diff = time_end - time_start
    system_info = get_sytem_info(time_diff)

    video_name = get_video_name()
    save_path = f"output/{video_name}_transcription.csv"
    df_results = pd.DataFrame(result_dict)
    df_results.to_csv(save_path)

    for file in os.listdir():
        if file.endswith(f".{VIDEO_FORMAT}"):
            os.rename(file, f"output/{file}")

    return df_results, system_info, save_path
