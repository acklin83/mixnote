import os
import json
from pydub import AudioSegment


def generate_peaks(audio_path: str, target_samples: int = 800) -> tuple[list[float], float]:
    """Generate normalized peak data for waveform visualization."""
    audio = AudioSegment.from_file(audio_path)
    duration = len(audio) / 1000.0

    samples = audio.get_array_of_samples()
    total = len(samples)

    if total == 0:
        return [0.0] * target_samples, duration

    chunk_size = max(1, total // target_samples)
    max_possible = float(2 ** (audio.sample_width * 8 - 1))

    peaks = []
    for i in range(target_samples):
        start = i * chunk_size
        end_idx = min(start + chunk_size, total)
        if start >= total:
            peaks.append(0.0)
            continue
        chunk = samples[start:end_idx]
        peak = max(abs(s) for s in chunk) if chunk else 0
        peaks.append(min(1.0, peak / max_possible))

    return peaks, duration


def get_or_generate_peaks(audio_path: str, cache_path: str, target_samples: int = 800) -> dict:
    """Get peaks from cache or generate and cache them."""
    if os.path.exists(cache_path):
        if os.path.getmtime(cache_path) >= os.path.getmtime(audio_path):
            with open(cache_path, "r") as f:
                return json.load(f)

    peaks, duration = generate_peaks(audio_path, target_samples)
    result = {"peaks": peaks, "duration": duration}

    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, "w") as f:
        json.dump(result, f)

    return result
