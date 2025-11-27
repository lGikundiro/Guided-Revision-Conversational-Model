"""Data acquisition helpers for the UrbanSound8K dataset.

This script attempts to download UrbanSound8K from Zenodo and organize the files
into `data/raw/UrbanSound8K` and create `data/train` and `data/test` folders
organized by class name using folds 1-8 for training and 9-10 for testing.

If automatic download fails (because of network or Zenodo changes), the script
prints instructions to manually download the dataset and place it under
`data/raw/UrbanSound8K`.
"""
from __future__ import annotations

import os
import tarfile
import shutil
from pathlib import Path
import requests
from tqdm import tqdm
import pandas as pd


ZENODO_URL = (
    "https://zenodo.org/record/1203745/files/UrbanSound8K.tar.gz?download=1"
)


def download_file(url: str, dest: Path, chunk_size: int = 1024 * 1024) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with open(dest, "wb") as f, tqdm(total=total, unit="iB", unit_scale=True) as bar:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))


def extract_tar(tar_path: Path, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    with tarfile.open(tar_path) as tar:
        tar.extractall(path=dest_dir)


def organize_urbansound8k(raw_dir: Path, out_train: Path, out_test: Path) -> None:
    """Organize UrbanSound8K audio files into train/test folders by class.

    Uses folds 1-8 as training, folds 9-10 as testing.
    """
    metadata_csv = raw_dir / "metadata" / "UrbanSound8K.csv"
    if not metadata_csv.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_csv}")

    df = pd.read_csv(metadata_csv)

    audio_root = raw_dir / "audio"
    if not audio_root.exists():
        raise FileNotFoundError(f"Audio folder not found under {raw_dir}")

    # Create destination folders
    for p in (out_train, out_test):
        p.mkdir(parents=True, exist_ok=True)

    # Iterate rows and copy files to class folders
    for idx, row in df.iterrows():
        fold = int(row["fold"])
        fname = row["slice_file_name"]
        cls = row["class"]
        src = audio_root / f"fold{fold}" / fname
        if not src.exists():
            # skip missing files but log
            print(f"Missing file: {src}")
            continue

        dest_root = out_train if fold <= 8 else out_test
        dest_dir = dest_root / cls
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / fname)


def prepare_urbansound8k(work_dir: Path = Path(".")) -> None:
    work_dir = Path(work_dir).resolve()
    raw_parent = work_dir / "data" / "raw"
    raw_dir = raw_parent / "UrbanSound8K"
    tar_dest = raw_parent / "UrbanSound8K.tar.gz"

    if raw_dir.exists():
        print(f"UrbanSound8K already present at {raw_dir}")
    else:
        print("Attempting to download UrbanSound8K from Zenodo...")
        try:
            download_file(ZENODO_URL, tar_dest)
            print("Download complete, extracting...")
            extract_tar(tar_dest, raw_parent)
            print("Extraction complete.")
            # cleanup tar
            try:
                tar_dest.unlink()
            except Exception:
                pass
        except Exception as e:
            print("Automatic download failed:", e)
            print("Please download UrbanSound8K manually from:")
            print("https://zenodo.org/record/1203745")
            print(f"Place the extracted folder at: {raw_dir}")
            return

    # Organize into train/test
    out_train = work_dir / "data" / "train"
    out_test = work_dir / "data" / "test"
    print("Organizing files into train/test folders (folds 1-8 train, 9-10 test)...")
    organize_urbansound8k(raw_dir, out_train, out_test)
    print("Organization complete.")


if __name__ == "__main__":
    prepare_urbansound8k()
