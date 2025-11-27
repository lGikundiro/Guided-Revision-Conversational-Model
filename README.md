# Guided-Revision-Conversational-Model

End-to-end ML pipeline for urban sound classification using UrbanSound8K dataset.

## 📋 Project Description

This project demonstrates a complete machine learning pipeline for audio classification:
- **Dataset**: UrbanSound8K (10 urban sound classes: air_conditioner, car_horn, children_playing, dog_bark, drilling, engine_idling, gun_shot, jackhammer, siren, street_music)
- **Model**: CNN trained on mel-spectrogram features
- **Framework**: TensorFlow/Keras
- **API**: FastAPI for predictions and retraining
- **UI**: Streamlit dashboard with visualizations
- **Deployment**: Docker + Render cloud platform
- **Load Testing**: Locust for performance analysis

## 🎥 Demo

**YouTube Demo**: [Add your video link here]

**Live URL**: [Add your deployed Render URL here]

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**
   ```powershell
   git clone https://github.com/lGikundiro/Guided-Revision-Conversational-Model.git
   cd Guided-Revision-Conversational-Model
   ```

2. **Create virtual environment and install dependencies**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Download and prepare UrbanSound8K dataset**
   ```powershell
   python src/data_preprocessing.py
   ```
   
   If automatic download fails, manually download from [Zenodo](https://zenodo.org/record/1203745) and extract to `data/raw/UrbanSound8K`.

4. **Train the model** (or open the notebook)
   
   **Option A - Using Jupyter Notebook** (recommended):
   ```powershell
   jupyter notebook notebook/project_notebook.ipynb
   ```
   
   **Option B - Command line**:
   ```powershell
   # Preprocess data
   python src/preprocessing.py --source data/raw/UrbanSound8K --out data/processed
   
   # Train model
   python src/model.py --data data/processed --model_output models/us8k_cnn.h5 --train --epochs 30
   ```

## 📊 Repository Structure

```
Guided-Revision-Conversational-Model/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Multi-service orchestration
│
├── notebook/
│   └── project_notebook.ipynb  # Complete training/evaluation notebook
│
├── src/
│   ├── data_preprocessing.py   # Download & organize dataset
│   ├── preprocessing.py        # Audio → mel-spectrogram conversion
│   ├── model.py               # Model training & evaluation
│   ├── prediction.py          # FastAPI server
│   └── ui.py                  # Streamlit dashboard
│
├── loadtest/
│   └── locustfile.py          # Load testing script
│
├── data/
│   ├── raw/                   # Raw UrbanSound8K dataset
│   ├── train/                 # Organized training data
│   └── test/                  # Organized test data
│
└── models/
    ├── us8k_cnn.h5           # Trained model
    └── classes.joblib        # Class label mappings
```

## 🎯 Features

### ✅ Implemented Functionalities

1. **Data Acquisition**
   - Automated UrbanSound8K download and extraction
   - Train/test split (folds 1-8 train, 9-10 test)
   - Class-organized folder structure

2. **Preprocessing**
   - Audio loading and normalization
   - Mel-spectrogram extraction (128 mel bands, 4 sec duration)
   - Padding/truncation for fixed-length inputs

3. **Model Training**
   - CNN architecture with BatchNorm and Dropout
   - Early stopping and learning rate reduction
   - Comprehensive evaluation metrics

4. **Model Evaluation** (in notebook)
   - Accuracy, Precision, Recall, F1-Score
   - Confusion matrix (raw and normalized)
   - ROC curves and AUC scores
   - Per-class performance analysis
   - Training history visualizations

5. **Prediction API** (`src/prediction.py`)
   - Single audio file prediction endpoint
   - Health check endpoint
   - Background retraining trigger

6. **UI Dashboard** (`src/ui.py`)
   - Single prediction interface
   - Bulk upload for retraining data
   - Retrain trigger button
   - Model health/uptime monitoring

7. **Containerization**
   - Dockerfile for API service
   - docker-compose.yml for multi-service deployment

8. **Load Testing**
   - Locust script for request flooding
   - Latency and throughput measurement

## 🏃 Running the Application

### Local Development

**Start FastAPI server:**
```powershell
python -m uvicorn src.prediction:app --host 0.0.0.0 --port 8000 --reload
```

**Start Streamlit UI:**
```powershell
streamlit run src/ui.py --server.port 8501
```

Access:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- UI: http://localhost:8501

### Docker Deployment

**Build and run with docker-compose:**
```powershell
docker-compose up --build
```

Access:
- API: http://localhost:8000
- UI: http://localhost:8501

**Scale API containers for load testing:**
```powershell
docker-compose up --scale api=3
```

## 🧪 Load Testing with Locust

1. **Prepare a sample audio file**
   ```powershell
   # Copy a test file to data/sample.wav for Locust
   cp data/test/air_conditioner/*.wav data/sample.wav
   ```

2. **Run Locust**
   ```powershell
   locust -f loadtest/locustfile.py --host=http://localhost:8000
   ```

3. **Access Locust UI**: http://localhost:8089

4. **Configure test**:
   - Number of users: 100
   - Spawn rate: 10/sec
   - Run test and observe latency/throughput

### Load Test Results

**Test Configuration**:
- Container count: 1, 2, 3
- Users: 100 concurrent
- Duration: 5 minutes

| Containers | Avg Response Time (ms) | Requests/sec | P95 Latency (ms) |
|-----------|----------------------|-------------|----------------|
| 1         | [TBD]                | [TBD]       | [TBD]          |
| 2         | [TBD]                | [TBD]       | [TBD]          |
| 3         | [TBD]                | [TBD]       | [TBD]          |

*Run load tests and update this table with your results*

## ☁️ Cloud Deployment (Render)

### Deploy to Render

1. **Push code to GitHub**
   ```powershell
   git add .
   git commit -m "Complete ML pipeline"
   git push origin main
   ```

2. **Create Render account**: https://render.com

3. **Create new Web Service**
   - Connect GitHub repository
   - Select branch: `main`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn src.prediction:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3.10

4. **Set environment variables**:
   - `MODEL_PATH`: `/app/models/us8k_cnn.h5`
   - `CLASSES_PATH`: `/app/models/classes.joblib`

5. **Deploy** and note the public URL

### Deploy Streamlit UI (separate service)

1. **Create another Web Service on Render**
   - Same repository
   - Start command: `streamlit run src/ui.py --server.port $PORT --server.address 0.0.0.0`

2. **Set environment variables**:
   - `api_url`: [Your API service URL from step 3]

### Monitoring

Render provides built-in:
- Service logs
- Metrics dashboard (CPU, memory, requests)
- Auto-scaling options

## 📈 Model Performance

**Validation Metrics** (from notebook):
- **Accuracy**: ~XX% (run notebook to get actual value)
- **Precision**: ~XX%
- **Recall**: ~XX%
- **F1-Score**: ~XX%
- **Average AUC**: ~XX

**Best Performing Classes**: [Add after training]
**Challenging Classes**: [Add after training]

See `notebook/project_notebook.ipynb` for detailed evaluation and visualizations.

## 🔄 Retraining the Model

### Via API
```powershell
curl -X POST http://localhost:8000/retrain
```

### Via UI
1. Upload new audio files (zip archive)
2. Click "Trigger retrain" button
3. Monitor training progress in API logs

### Manual
```powershell
python src/model.py --data data/processed --model_output models/us8k_cnn_v2.h5 --train --epochs 10
```

## 🛠️ Development

### Adding New Features

1. Update `src/` modules
2. Add tests if applicable
3. Update notebook if training logic changes
4. Rebuild Docker image:
   ```powershell
   docker-compose build
   ```

### Troubleshooting

**Issue**: Model not loading
- Ensure `models/us8k_cnn.h5` exists
- Check file paths in environment variables

**Issue**: Audio file upload fails
- Verify file format is `.wav`
- Check file size (<10MB recommended)

**Issue**: Locust can't find sample.wav
- Copy a test file: `cp data/test/siren/*.wav data/sample.wav`

## 📚 Technologies Used

- **ML**: TensorFlow, Keras, librosa, scikit-learn
- **API**: FastAPI, uvicorn
- **UI**: Streamlit
- **Data**: NumPy, Pandas
- **Visualization**: Matplotlib, Seaborn
- **Load Testing**: Locust
- **Deployment**: Docker, Render

## 📄 License

MIT License - see LICENSE file for details

## 👤 Author

**Liliane Gikundiro**
- GitHub: [@lGikundiro](https://github.com/lGikundiro)

## 🙏 Acknowledgments

- UrbanSound8K dataset: J. Salamon, C. Jacoby and J. P. Bello
- TensorFlow team
- Render platform
# Guided-Revision-Conversational-Model

Audio classification end-to-end demo using UrbanSound8K. This repo contains code to preprocess audio, train a TensorFlow/Keras model on mel-spectrograms, serve predictions via a FastAPI endpoint, provide a Streamlit UI for uploads and retraining, and scripts for load testing with Locust. The project is prepared for deployment on Render (instructions below).

Features
- Data acquisition script / instructions for UrbanSound8K
- Preprocessing: convert .wav to mel-spectrograms
- Model: simple Keras CNN for audio classification
- API: FastAPI app with `/predict` and `/retrain` endpoints
- UI: Streamlit app for single prediction, bulk upload, visualizations and retrain trigger
- Containerization: `Dockerfile` and `docker-compose.yml`
- Load testing: `loadtest/locustfile.py`

Getting started (local)
1. Install Python 3.10+ and create a virtual environment
```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2. Download UrbanSound8K and place it under `data/UrbanSound8K/` (see `scripts/download_data.py` for an automated attempt).

3. Preprocess data and run a quick training (this may take time):
```powershell
python -m src.preprocessing --source data/UrbanSound8K --out data/processed --n_mels 128 --duration 4.0
python -m src.model --train --data data/processed --model_output models/us8k_cnn.h5
```

4. Run the API
```powershell
uvicorn src.prediction:app --host 0.0.0.0 --port 8000
```

5. Run the Streamlit UI
```powershell
streamlit run src/ui.py
```

Deployment (Render)
- Build Docker images from the provided `Dockerfile` and push to a container registry or connect your Render service to this repository. See `docker-compose.yml` for service layout.

Repository structure
```
Project_name/
├── README.md
├── requirements.txt
├── notebook/
│   └── project_notebook.ipynb
├── src/
│   ├── preprocessing.py
   ├── model.py
   ├── prediction.py
   └── ui.py
├── data/
│   ├── UrbanSound8K/   # raw dataset (not committed)
│   └── processed/      # generated by preprocessing
├── models/
│   └── us8k_cnn.h5
└── loadtest/
    └── locustfile.py
```

Notes
- UrbanSound8K is large; training locally may be slow. For a demo use a subset or train on a cloud instance with a GPU.
- The repository scripts are written for clarity and reproducibility; adapt hyperparameters as needed.
