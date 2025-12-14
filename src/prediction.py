"""FastAPI prediction server for audio uploads"""
import os
import io
import numpy as np
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
import uvicorn
import librosa
import tensorflow as tf
import joblib
from threading import Thread

MODEL_PATH = os.environ.get('MODEL_PATH', 'models/us8k_cnn.h5')
CLASSES_PATH = os.environ.get('CLASSES_PATH', 'models/classes.joblib')

app = FastAPI()
model = None
classes = None


def load_model():
    global model, classes
    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
    if os.path.exists(CLASSES_PATH):
        classes = joblib.load(CLASSES_PATH)


@app.on_event('startup')
def startup_event():
    load_model()


@app.get('/')
def root():
    return {
        'message': 'Audio Classification API',
        'endpoints': {
            'GET /': 'API information',
            'GET /health': 'Health check',
            'POST /predict': 'Predict audio class (upload .wav file)',
            'POST /retrain': 'Trigger model retraining'
        },
        'model_loaded': model is not None,
        'classes': classes if classes else []
    }


def prepare_mel_from_bytes(file_bytes, sr=22050, n_mels=128, duration=4.0):
    data, sr = librosa.load(io.BytesIO(file_bytes), sr=sr, mono=True, duration=duration)
    target_length = int(sr * duration)
    if data.shape[0] < target_length:
        data = np.pad(data, (0, target_length - data.shape[0]))
    else:
        data = data[:target_length]
    mel = librosa.feature.melspectrogram(data, sr=sr, n_mels=n_mels)
    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_norm = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-6)
    return mel_norm.astype(np.float32)


@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    global model, classes
    if model is None or classes is None:
        return JSONResponse({'error': 'Model not loaded'}, status_code=500)
    body = await file.read()
    try:
        mel = prepare_mel_from_bytes(body)
        x = np.expand_dims(mel, axis=0)
        preds = model.predict(x)
        idx = int(np.argmax(preds, axis=1)[0])
        return {'prediction': classes[idx], 'probs': preds.tolist()[0]}
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)


def retrain_background(data_dir='data/processed', model_output='models/us8k_cnn.h5'):
    # lightweight retrain: call the model.train routine in a thread
    from src.model import train
    train(data_dir, model_output, epochs=3)
    # reload model after training
    load_model()


@app.post('/retrain')
async def retrain(background_tasks: BackgroundTasks):
    background_tasks.add_task(retrain_background)
    return {'status': 'retraining_started'}


@app.get('/health')
def health():
    return {'status': 'ok', 'model_loaded': model is not None}


if __name__ == '__main__':
    uvicorn.run('src.prediction:app', host='0.0.0.0', port=8000, reload=True)
