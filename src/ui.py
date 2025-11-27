"""Streamlit UI for single prediction, bulk upload and retrain trigger"""
import streamlit as st
import requests
import zipfile
import os
from io import BytesIO

# Get API URL from environment or use default
API_URL = os.environ.get('api_url', 'http://localhost:8000')

st.set_page_config(page_title="UrbanSound8K Classifier", page_icon="🔊", layout="wide")

st.title('🔊 UrbanSound8K - Audio Classifier')
st.markdown("""
This application classifies urban sounds into 10 categories:
**air_conditioner, car_horn, children_playing, dog_bark, drilling, 
engine_idling, gun_shot, jackhammer, siren, street_music**
""")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("""
    **ML Pipeline Demo**
    
    - Dataset: UrbanSound8K
    - Model: CNN on mel-spectrograms
    - Framework: TensorFlow/Keras
    """)
    
    st.header("Model Status")
    try:
        health_resp = requests.get(f'{API_URL}/health', timeout=5)
        if health_resp.ok:
            health_data = health_resp.json()
            if health_data.get('model_loaded'):
                st.success("✅ Model loaded")
            else:
                st.error("❌ Model not loaded")
            st.json(health_data)
        else:
            st.error(f"API Error: {health_resp.status_code}")
    except Exception as e:
        st.error(f"Cannot reach API: {str(e)}")
        st.warning(f"Trying to connect to: {API_URL}")

# Main content
tab1, tab2, tab3 = st.tabs(["🎵 Single Prediction", "📦 Bulk Upload", "📊 Visualizations"])

with tab1:
    st.header('Single Audio Prediction')
    st.write("Upload a WAV file to classify the urban sound.")
    
    audio_file = st.file_uploader('Choose a WAV file', type=['wav'], key='single_pred')
    
    if audio_file is not None:
        # Display audio player
        st.audio(audio_file, format='audio/wav')
        
        if st.button('🔍 Predict', type='primary'):
            with st.spinner('Analyzing audio...'):
                try:
                    files = {'file': (audio_file.name, audio_file.getvalue(), 'audio/wav')}
                    resp = requests.post(f'{API_URL}/predict', files=files, timeout=30)
                    
                    if resp.ok:
                        result = resp.json()
                        st.success(f"**Prediction: {result['prediction']}**")
                        
                        # Show probabilities
                        st.subheader("Class Probabilities")
                        probs = result.get('probs', [])
                        if probs:
                            import pandas as pd
                            classes = ['air_conditioner', 'car_horn', 'children_playing', 
                                     'dog_bark', 'drilling', 'engine_idling', 
                                     'gun_shot', 'jackhammer', 'siren', 'street_music']
                            prob_df = pd.DataFrame({
                                'Class': classes[:len(probs)],
                                'Probability': probs
                            }).sort_values('Probability', ascending=False)
                            
                            st.bar_chart(prob_df.set_index('Class'))
                            st.dataframe(prob_df, use_container_width=True)
                    else:
                        st.error(f"Prediction failed: {resp.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with tab2:
    st.header('Bulk Upload for Retraining')
    st.write("Upload a ZIP file containing WAV files to add to the training dataset.")
    
    zip_file = st.file_uploader('Upload a ZIP of WAV files', type=['zip'], key='bulk_upload')
    
    if zip_file is not None:
        st.info(f"Uploaded: {zip_file.name} ({zip_file.size / 1024:.2f} KB)")
        
        if st.button('📤 Extract Files', type='secondary'):
            with st.spinner('Extracting files...'):
                try:
                    z = zipfile.ZipFile(BytesIO(zip_file.getvalue()))
                    extract_dir = os.path.join('data', 'uploads')
                    os.makedirs(extract_dir, exist_ok=True)
                    z.extractall(extract_dir)
                    
                    # Count extracted files
                    wav_files = [f for f in z.namelist() if f.endswith('.wav')]
                    st.success(f'✅ Extracted {len(wav_files)} WAV files to {extract_dir}')
                    st.write("Files:", wav_files[:10])  # Show first 10
                    if len(wav_files) > 10:
                        st.write(f"... and {len(wav_files) - 10} more")
                except Exception as e:
                    st.error(f"Extraction failed: {str(e)}")
    
    st.divider()
    st.subheader("Trigger Model Retraining")
    st.warning("⚠️ Retraining will run in the background and may take several minutes.")
    
    if st.button('🔄 Trigger Retrain', type='primary'):
        with st.spinner('Starting retraining process...'):
            try:
                resp = requests.post(f'{API_URL}/retrain', timeout=10)
                if resp.ok:
                    st.success('✅ Retraining started! Check API logs for progress.')
                    st.json(resp.json())
                else:
                    st.error(f"Retrain failed: {resp.text}")
            except Exception as e:
                st.error(f"Error triggering retrain: {str(e)}")

with tab3:
    st.header('Dataset Visualizations')
    st.write("Insights about the UrbanSound8K dataset and model performance.")
    
    st.subheader("📊 Class Distribution")
    st.info("The UrbanSound8K dataset contains 10 urban sound classes with roughly balanced distribution (~800-1000 samples per class).")
    
    # Placeholder for actual visualizations - would load from saved analysis
    st.write("""
    **Key Insights:**
    - All 10 classes are well-represented
    - Balanced dataset means no need for class weighting
    - Total samples: ~8,700+ audio clips
    """)
    
    st.subheader("🎯 Model Performance")
    st.write("See the Jupyter notebook (`notebook/project_notebook.ipynb`) for detailed evaluation metrics including:")
    st.markdown("""
    - ✅ Accuracy, Precision, Recall, F1-Score
    - ✅ Confusion Matrix
    - ✅ ROC Curves and AUC
    - ✅ Per-class performance analysis
    - ✅ Training history plots
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center'>
    <p>Built with Streamlit | ML Model: TensorFlow/Keras | Dataset: UrbanSound8K</p>
</div>
""", unsafe_allow_html=True)
