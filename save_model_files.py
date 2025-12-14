"""Save model and necessary files for deployment"""
import joblib
from pathlib import Path

# Create models directory
models_dir = Path("models")
models_dir.mkdir(exist_ok=True)

# Save class mappings
class_names = ['car_horn', 'dog_bark', 'drilling', 'siren', 'street_music']
label_to_idx = {name: i for i, name in enumerate(class_names)}
idx_to_label = {i: name for i, name in enumerate(class_names)}

classes_path = models_dir / "classes.joblib"
joblib.dump(class_names, classes_path)
print(f"Class mappings saved to {classes_path}")

# Save label mappings
mappings_path = models_dir / "label_mappings.joblib"
joblib.dump({'label_to_idx': label_to_idx, 'idx_to_label': idx_to_label}, mappings_path)
print(f"Label mappings saved to {mappings_path}")

print("\nModel files ready for deployment!")
print(f"Model: models/us8k_cnn.h5")
print(f"Classes: models/classes.joblib")
print(f"Mappings: models/label_mappings.joblib")
