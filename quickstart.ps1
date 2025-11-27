# Quick Start Script for Windows PowerShell
# Run this script to set up and test the project locally

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "UrbanSound8K ML Pipeline - Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python
Write-Host "[1/7] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.10+ from python.org" -ForegroundColor Red
    exit 1
}

# Step 2: Create virtual environment
Write-Host "[2/7] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv .venv
    Write-Host "✓ Created .venv" -ForegroundColor Green
}

# Step 3: Activate and install dependencies
Write-Host "[3/7] Activating environment and installing dependencies..." -ForegroundColor Yellow
Write-Host "   (This may take a few minutes)" -ForegroundColor Gray
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Step 4: Check data
Write-Host "[4/7] Checking dataset..." -ForegroundColor Yellow
if (Test-Path "data\train") {
    $trainFiles = (Get-ChildItem -Path "data\train" -Recurse -Filter "*.wav").Count
    Write-Host "✓ Found $trainFiles training files" -ForegroundColor Green
} else {
    Write-Host "⚠ Training data not found" -ForegroundColor Yellow
    Write-Host "   Run: python src\data_preprocessing.py" -ForegroundColor Gray
}

# Step 5: Check model
Write-Host "[5/7] Checking trained model..." -ForegroundColor Yellow
if (Test-Path "models\us8k_cnn.h5") {
    $modelSize = (Get-Item "models\us8k_cnn.h5").Length / 1MB
    Write-Host "✓ Found model (${modelSize:N2} MB)" -ForegroundColor Green
} else {
    Write-Host "⚠ Model not found" -ForegroundColor Yellow
    Write-Host "   Train using: jupyter notebook notebook\project_notebook.ipynb" -ForegroundColor Gray
}

# Step 6: Instructions
Write-Host ""
Write-Host "[6/7] Quick Commands:" -ForegroundColor Cyan
Write-Host "   Download data:  python src\data_preprocessing.py" -ForegroundColor White
Write-Host "   Train model:    jupyter notebook notebook\project_notebook.ipynb" -ForegroundColor White
Write-Host "   Start API:      python -m uvicorn src.prediction:app --reload" -ForegroundColor White
Write-Host "   Start UI:       streamlit run src\ui.py" -ForegroundColor White
Write-Host "   Run tests:      locust -f loadtest\locustfile.py --host=http://localhost:8000" -ForegroundColor White
Write-Host "   Docker:         docker-compose up --build" -ForegroundColor White

# Step 7: Next steps
Write-Host ""
Write-Host "[7/7] Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Run data acquisition if needed" -ForegroundColor White
Write-Host "   2. Open and run the Jupyter notebook to train" -ForegroundColor White
Write-Host "   3. Start API and UI in separate terminals" -ForegroundColor White
Write-Host "   4. Test predictions via http://localhost:8501" -ForegroundColor White
Write-Host "   5. Deploy to Render using DEPLOYMENT.md guide" -ForegroundColor White

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! 🎉" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
