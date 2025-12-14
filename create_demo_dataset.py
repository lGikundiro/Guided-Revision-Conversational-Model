"""Create a small demo dataset for testing the pipeline without full UrbanSound8K download"""
import numpy as np
import soundfile as sf
from pathlib import Path
import pandas as pd

# Create demo dataset structure
data_dir = Path("data")
train_dir = data_dir / "train"
test_dir = data_dir / "test"
raw_dir = data_dir / "raw" / "UrbanSound8K"
metadata_dir = raw_dir / "metadata"

# Create directories
for class_name in ["dog_bark", "siren", "car_horn", "street_music", "drilling"]:
    (train_dir / class_name).mkdir(parents=True, exist_ok=True)
    (test_dir / class_name).mkdir(parents=True, exist_ok=True)

metadata_dir.mkdir(parents=True, exist_ok=True)

# Generate synthetic audio samples (simple sine waves with noise)
sr = 22050
duration = 4.0
samples = int(sr * duration)

frequencies = {
    "dog_bark": [300, 800, 1500],  # Multiple frequencies for barking
    "siren": [400, 1200],  # Alternating siren tones
    "car_horn": [500],  # Single tone
    "street_music": [440, 554, 659],  # Musical notes (A, C#, E)
    "drilling": [200, 600, 1000]  # Mechanical drilling sounds
}

print("Generating demo audio files...")
metadata_rows = []
file_id = 0

for split, split_dir in [("train", train_dir), ("test", test_dir)]:
    n_samples = 20 if split == "train" else 5
    
    for class_name, freqs in frequencies.items():
        class_dir = split_dir / class_name
        
        for i in range(n_samples):
            # Generate audio with multiple frequency components
            audio = np.zeros(samples)
            for freq in freqs:
                t = np.linspace(0, duration, samples)
                # Add sine wave with some amplitude variation
                audio += 0.3 * np.sin(2 * np.pi * freq * t) * (0.8 + 0.2 * np.random.random())
            
            # Add some noise for realism
            audio += 0.1 * np.random.randn(samples)
            
            # Normalize
            audio = audio / np.max(np.abs(audio)) * 0.9
            
            # Save file
            filename = f"{class_name}_{file_id:04d}.wav"
            filepath = class_dir / filename
            sf.write(filepath, audio, sr)
            
            # Add to metadata
            fold = 1 if split == "train" else 9
            metadata_rows.append({
                'slice_file_name': filename,
                'fsID': file_id,
                'start': 0.0,
                'end': duration,
                'salience': 1,
                'fold': fold,
                'classID': list(frequencies.keys()).index(class_name),
                'class': class_name
            })
            
            file_id += 1
            
        print(f"Created {n_samples} {split} samples for {class_name}")

# Create metadata CSV
df = pd.DataFrame(metadata_rows)
metadata_path = metadata_dir / "UrbanSound8K.csv"
df.to_csv(metadata_path, index=False)
print(f"\nMetadata saved to {metadata_path}")
print(f"Total files created: {len(df)}")
print(f"Classes: {list(frequencies.keys())}")
print("\nDemo dataset ready!")
