"""Audio preprocessing utilities.

Provides helpers to load audio, compute log-mel spectrograms, and prepare lists
of files/labels for training. Designed to work with the dataset organized by
class subfolders under `data/train` and `data/test`.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Tuple, List

import numpy as np
import librosa


def load_audio(path: str | Path, sr: int = 22050, duration: float = 4.0) -> np.ndarray:
    """Load an audio file and return a mono waveform of fixed length.

    Args:
        path: Path to audio file.
        sr: Target sampling rate.
        duration: Duration in seconds for output waveform. Audio shorter than
            this will be zero-padded; longer audio will be truncated.

    Returns:
        1D numpy array of length `sr * duration`.
    """
    path = str(path)
    target_len = int(sr * duration)
    y, _ = librosa.load(path, sr=sr, mono=True)
    if y.shape[0] > target_len:
        y = y[:target_len]
    elif y.shape[0] < target_len:
        pad_width = target_len - y.shape[0]
        y = np.pad(y, (0, pad_width), mode="constant")
    return y


def compute_log_mel(waveform: np.ndarray, sr: int = 22050, n_mels: int = 128,
                    n_fft: int = 2048, hop_length: int = 512) -> np.ndarray:
    """Compute log-mel spectrogram from a waveform.

    Returns:
        2D numpy array (n_mels, time_frames) with log-amplitude scaled values.
    """
    S = librosa.feature.melspectrogram(y=waveform, sr=sr, n_fft=n_fft,
                                       hop_length=hop_length, n_mels=n_mels)
    log_S = librosa.power_to_db(S, ref=np.max)
    return log_S


def list_files_and_labels(root_dir: str | Path) -> Tuple[List[str], List[str]]:
    """Walk `root_dir` and gather file paths and their class labels.

    Expects directory structure: root_dir/<class_name>/*.wav
    Returns two parallel lists: file paths and labels (class names).
    """
    root = Path(root_dir)
    if not root.exists():
        raise FileNotFoundError(f"Root directory not found: {root}")

    file_paths: List[str] = []
    labels: List[str] = []

    for class_dir in sorted([p for p in root.iterdir() if p.is_dir()]):
        cls = class_dir.name
        for audio_file in class_dir.glob("*.wav"):
            file_paths.append(str(audio_file))
            labels.append(cls)

    return file_paths, labels


def label_to_index(labels: List[str]) -> Tuple[dict, dict]:
    """Create mapping dicts label->index and index->label from label list."""
    unique = sorted(set(labels))
    l2i = {l: i for i, l in enumerate(unique)}
    i2l = {i: l for l, i in l2i.items()}
    return l2i, i2l


if __name__ == "__main__":
    # quick smoke test helpers (won't run in CI without dataset)
    d = Path("../data/train")
    if d.exists():
        fps, labs = list_files_and_labels(d)
        print(f"Found {len(fps)} files across {len(set(labs))} classes")
    else:
        print("No train data found at ../data/train. Run data_preprocessing first.")
"""Preprocessing utilities for UrbanSound8K -> mel-spectrograms

Usage (example):
python -m src.preprocessing --source data/UrbanSound8K --out data/processed --n_mels 128 --duration 4.0
"""
import os
import argparse
import numpy as np
import pandas as pd
import librosa
import soundfile as sf


def extract_mel(wav_path, sr=22050, n_mels=128, duration=4.0):
    y, sr = librosa.load(wav_path, sr=sr, mono=True, duration=duration)
    # pad or truncate
    target_length = int(sr * duration)
    if y.shape[0] < target_length:
        y = np.pad(y, (0, target_length - y.shape[0]))
    else:
        y = y[:target_length]
    mel = librosa.feature.melspectrogram(y, sr=sr, n_mels=n_mels)
    mel_db = librosa.power_to_db(mel, ref=np.max)
    # normalize to 0-1
    mel_norm = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-6)
    return mel_norm.astype(np.float32)


def process_urbansound8k(source_dir, out_dir, n_mels=128, duration=4.0):
    os.makedirs(out_dir, exist_ok=True)
    meta_path = os.path.join(source_dir, 'metadata', 'UrbanSound8K.csv')
    if not os.path.exists(meta_path):
        # alternative location
        meta_alt = os.path.join(source_dir, 'UrbanSound8K.csv')
        if os.path.exists(meta_alt):
            meta_path = meta_alt
        else:
            raise FileNotFoundError('Could not find UrbanSound8K metadata CSV in expected locations')

    meta = pd.read_csv(meta_path)
    X = []
    y = []
    classes = sorted(meta['class'].unique())
    class_to_idx = {c: i for i, c in enumerate(classes)}

    for idx, row in meta.iterrows():
        fold = row.get('fold')
        file = row['slice_file_name']
        cls = row['class']
        if pd.isna(fold):
            continue
        audio_path = os.path.join(source_dir, f'fold{int(fold)}', file)
        if not os.path.exists(audio_path):
            continue
        try:
            mel = extract_mel(audio_path, n_mels=n_mels, duration=duration)
            X.append(mel)
            y.append(class_to_idx[cls])
        except Exception:
            continue

    X = np.array(X)
    y = np.array(y)
    print('Processed', X.shape, y.shape)
    np.save(os.path.join(out_dir, 'X.npy'), X)
    np.save(os.path.join(out_dir, 'y.npy'), y)
    # save classes
    pd.Series(classes).to_csv(os.path.join(out_dir, 'classes.csv'), index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--n_mels', type=int, default=128)
    parser.add_argument('--duration', type=float, default=4.0)
    args = parser.parse_args()
    process_urbansound8k(args.source, args.out, n_mels=args.n_mels, duration=args.duration)


if __name__ == '__main__':
    main()
