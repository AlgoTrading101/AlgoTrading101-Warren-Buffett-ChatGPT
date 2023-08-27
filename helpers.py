"""Helper functions."""
from datetime import timedelta
from typing import Dict

import psutil
from gpuinfo import GPUInfo


def convert_time(secs: float) -> timedelta:
    """Convert seconds to timedelta."""
    return timedelta(seconds=round(secs))


def prepare_output(segments: list) -> Dict[str, list]:
    """Prepare output for the transcription dataframe."""
    result_dict: Dict[str, list] = {"Start": [], "End": [], "Speaker": [], "Text": []}
    text = ""
    for i, segment in enumerate(segments):
        if i == 0 or segments[i - 1]["speaker"] != segment["speaker"]:
            result_dict["Start"].append(str(convert_time(segment["start"])))
            result_dict["Speaker"].append(segment["speaker"])
            if i != 0:
                result_dict["End"].append(str(convert_time(segments[i - 1]["end"])))
                result_dict["Text"].append(text)
                text = ""
        text += segment["text"] + " "
    result_dict["End"].append(str(convert_time(segments[i - 1]["end"])))
    result_dict["Text"].append(text)

    return result_dict


def get_sytem_info(time_diff: float) -> str:
    """Get system information."""
    memory = psutil.virtual_memory()
    gpu_utilization, gpu_memory = GPUInfo.gpu_usage()
    gpu_utilization = gpu_utilization[0] if len(gpu_utilization) > 0 else 0
    gpu_memory = gpu_memory[0] if len(gpu_memory) > 0 else 0
    system_info = (
        f"*Memory: {memory.total / (1024 * 1024 * 1024):.2f}GB,"
        f" used: {memory.percent}%, "
        f"available: {memory.available / (1024 * 1024 * 1024):.2f}GB.*\n"
        f"*Processing time: {time_diff:.5} seconds.*\n"
        f"*GPU Utilization: {gpu_utilization}%, GPU Memory: {gpu_memory}MiB.*"
    )

    return system_info


whisper_models = [
    "tiny.en",
    "tiny",
    "base.en",
    "base",
    "small.en",
    "small",
    "medium.en",
    "medium",
    "large-v1",
    "large-v2",
    "large",
]
