# 🍅 Tomato Leaf Disease Detection

A full-stack deep learning application that classifies tomato plant leaf diseases from uploaded images using a CNN model served via FastAPI and a React frontend.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Disease Classes](#disease-classes)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
  - [Backend (FastAPI)](#backend-fastapi)
  - [Frontend (React)](#frontend-react)
- [Running with TensorFlow Serving](#running-with-tensorflow-serving)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Model Information](#model-information)
- [Common Errors & Fixes](#common-errors--fixes)
- [Bug Fixes Applied](#bug-fixes-applied)

---

## Overview

This project uses a Convolutional Neural Network (CNN) trained on the [Kaggle Tomato Leaf Dataset](https://www.kaggle.com/datasets/kaustubhb999/tomatoleaf) to identify 10 types of tomato leaf conditions.

The application consists of:
- **Backend:** FastAPI server (`api/main.py`) that loads a TensorFlow SavedModel and exposes a `/predict` endpoint.
- **Frontend:** React app (`frontend/`) with a drag-and-drop image upload interface that displays the predicted disease class and confidence score.
- **TF Serving variant:** `api/main-tf-serving.py` for production deployments using TensorFlow Serving.

---

## Disease Classes

| # | Class Name |
|---|-----------|
| 1 | Bacterial Spot |
| 2 | Early Blight |
| 3 | Late Blight |
| 4 | Leaf Mold |
| 5 | Septoria Leaf Spot |
| 6 | Spider Mites (Two-spotted) |
| 7 | Target Spot |
| 8 | Tomato Yellow Leaf Curl Virus |
| 9 | Tomato Mosaic Virus |
| 10 | Healthy |

---

## Project Structure

```
Tomato_Leaf_Disease_Detection/
├── api/
│   ├── main.py                  # FastAPI server (direct TF model)
│   ├── main-tf-serving.py       # FastAPI server (TF Serving backend)
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── home.js              # Main UI component
│   │   ├── index.js
│   │   ├── index.css
│   │   ├── bg.png               # Background image
│   │   └── reportWebVitals.js
│   ├── .env                     # API URL config (create manually)
│   └── package.json
├── Models/
│   ├── 1/                       # TensorFlow SavedModel (used by main.py)
│   │   ├── saved_model.pb
│   │   └── variables/
│   ├── Tomatoes_Model.h5        # Keras H5 model (alternative)
│   └── Tomato_Model.pkl         # Pickle model (alternative)
├── Tomato.ipynb                 # Training notebook
├── package.json                 # Root scripts
└── README.md
```

---

## Prerequisites

- Python **3.9 – 3.11** (3.12+ is not supported by TensorFlow)
- Node.js **16+** and npm
  - ⚠️ If you are on Node.js 17+, see [Common Errors & Fixes](#common-errors--fixes)
- (Optional) Docker — for TensorFlow Serving

---

## Installation & Setup

### Backend (FastAPI)

> ⚠️ Make sure you are inside the `api/` folder before running these commands.

**1. Navigate to the `api/` directory:**
```bash
cd api
```

**2. Create and activate a virtual environment (recommended):**
```bash
# macOS/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```
Your terminal should show `(venv)` at the start of the line.

**3. Install dependencies:**
```bash
# Try one of these — use whichever works on your system
pip install -r requirements.txt
python -m pip install -r requirements.txt
py -m pip install -r requirements.txt
```

**4. Start the API server:**
```bash
# Try one of these
uvicorn main:app --reload --host 0.0.0.0 --port 8000
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
py -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**5. Verify it is running:**

Open this in your browser:
```
http://localhost:8000/ping
```
You should see:
```json
{ "status": "alive", "message": "Tomato Disease Detection API is running" }
```

> ⚠️ **Keep this terminal open.** The API must stay running while you use the app.

---

### Frontend (React)

> Open a **new terminal** for this — do not close the API terminal.

**1. Navigate to the `frontend/` directory:**
```bash
cd frontend
```

**2. Create the `.env` file** inside `frontend/`:

```bash
# Windows Command Prompt
echo REACT_APP_API_URL=http://localhost:8000/predict > .env

# macOS/Linux
echo "REACT_APP_API_URL=http://localhost:8000/predict" > .env
```

Or create the file manually and add this single line:
```
REACT_APP_API_URL=http://localhost:8000/predict
```

**3. Install dependencies:**
```bash
npm install
```
⏳ This may take 2–5 minutes the first time.

**4. Start the frontend:**

**Windows Command Prompt:**
```bash
set NODE_OPTIONS=--openssl-legacy-provider
npm start
```

**Windows PowerShell:**
```bash
$env:NODE_OPTIONS="--openssl-legacy-provider"
npm start
```

**macOS/Linux:**
```bash
npm start
```

**5. The app will open automatically at:**
```
http://localhost:3000
```

---

## Using the App

1. Open `http://localhost:3000` in your browser
2. Drag and drop a tomato leaf image onto the upload box (or click to browse)
3. Wait a moment while the image is sent to the API
4. The app displays the **disease name** and **confidence percentage**
5. Click **Clear** to upload another image

---

## Running with TensorFlow Serving

For production deployments, use TF Serving with Docker instead of loading the model directly in Python.

**1. Start TF Serving via Docker:**
```bash
docker run -t --rm \
  -p 8501:8501 \
  -v "$(pwd)/Models:/models/tomatoes_model" \
  -e MODEL_NAME=tomatoes_model \
  tensorflow/serving
```

**2. Start the TF Serving-backed API:**
```bash
cd api
python -m uvicorn main-tf-serving:app --reload --host 0.0.0.0 --port 8000
```

**3. Start the frontend** the same way as above — no changes needed.

---

## Environment Variables

| Variable | Description |
|---|---|
| `REACT_APP_API_URL` | Full URL to the `/predict` endpoint, e.g. `http://localhost:8000/predict` |

---

## API Reference

### `GET /ping`

Health check endpoint.

**Response:**
```json
{
  "status": "alive",
  "message": "Tomato Disease Detection API is running"
}
```

---

### `POST /predict`

Upload a tomato leaf image for classification.

**Request:** `multipart/form-data`

| Field | Type | Description |
|---|---|---|
| `file` | image file | A JPEG, PNG, or WebP image of a tomato plant leaf |

**Response:**
```json
{
  "class": "Early_blight",
  "confidence": 0.9732,
  "confidence_percent": "97.32%"
}
```

**Error Responses:**

| Status | Reason |
|---|---|
| `400` | Uploaded file is not an image |
| `503` | Cannot connect to TF Serving (tf-serving variant only) |

---

## Model Information

- **Architecture:** Convolutional Neural Network (CNN)
- **Input Shape:** `256 × 256 × 3` (RGB)
- **Output:** Softmax probabilities over 10 disease classes
- **Training Dataset:** [Kaggle Tomato Leaf Dataset](https://www.kaggle.com/datasets/kaustubhb999/tomatoleaf)
- **Saved Format:** TensorFlow SavedModel (`Models/1/`)

To retrain on a custom dataset, open `Tomato.ipynb` and follow the notebook steps. After training, save the model to `Models/1/` to have it automatically loaded by the API.

---

## Common Errors & Fixes

### ❌ `'pip' is not recognized`
```bash
# Use python -m pip instead
python -m pip install -r requirements.txt

# Or with py launcher (Windows)
py -m pip install -r requirements.txt
```

---

### ❌ `'uvicorn' is not recognized`
```bash
# Use python -m uvicorn instead
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

### ❌ `error:0308010C:digital envelope routines::unsupported`

This happens when using **Node.js 17 or higher** with `react-scripts 4`.

**Quick fix — Windows Command Prompt:**
```bash
set NODE_OPTIONS=--openssl-legacy-provider
npm start
```

**Quick fix — Windows PowerShell:**
```bash
$env:NODE_OPTIONS="--openssl-legacy-provider"
npm start
```

**Quick fix — macOS/Linux:**
```bash
export NODE_OPTIONS=--openssl-legacy-provider
npm start
```

**Permanent fix** — update the `"scripts"` section in `frontend/package.json`:
```json
"scripts": {
  "start": "react-scripts --openssl-legacy-provider start",
  "build": "react-scripts --openssl-legacy-provider build",
  "test": "react-scripts test",
  "eject": "react-scripts eject"
}
```

---

### ❌ TensorFlow install fails

Make sure you are using **Python 3.9, 3.10, or 3.11**. TensorFlow does not support Python 3.12+.
```bash
python --version
```
If needed, download Python 3.11 from https://www.python.org/downloads/

---

### ❌ Prediction always fails / CORS error

- Make sure the backend API is running on port `8000`
- Make sure the `.env` file exists inside the `frontend/` folder with:
  ```
  REACT_APP_API_URL=http://localhost:8000/predict
  ```
- Restart the frontend after creating or editing the `.env` file

---

### ❌ `uvicorn` not found after installing

You may have installed into a different Python environment. Always activate your virtual environment first:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

---

## Bug Fixes Applied

| File | Bug | Fix |
|---|---|---|
| `api/main-tf-serving.py` | Endpoint pointed to `potatoes_model` instead of `tomatoes_model` | Corrected model name |
| `api/main.py` | `host='localhost'` blocks external access | Changed to `host='0.0.0.0'` |
| `api/main.py` | No image validation — any file type accepted | Added `content_type` check, returns HTTP 400 for non-images |
| `api/main.py` | Images not resized before prediction | Added resize to `256×256` and RGB conversion |
| `api/main-tf-serving.py` | No error handling for TF Serving failures | Added `try/except` with HTTP 503/502 responses |
| `api/requirements.txt` | `tensorflow-serving-api==2.5.0` conflicts with `tensorflow==2.15.0` | Removed conflicting package; added `requests` |
| `frontend/src/home.js` | `<CardMedia component="image">` is invalid HTML | Corrected to `component="img"` |
| `frontend/src/home.js` | Import `image` shadowed the `image` state variable | Renamed import to `bgImage` |
| `frontend/src/home.js` | `require("axios")` used in module scope | Replaced with `import axios from "axios"` |
| `frontend/src/home.js` | No error handling for failed API calls | Added `try/catch` with visible error message |
| `frontend/src/home.js` | Object URL never revoked — memory leak | Added `URL.revokeObjectURL()` cleanup in `useEffect` |
| `frontend/package.json` | Package name was generic `"photo"` | Renamed to `tomato-leaf-disease-detection` |
| `package.json` (root) | Contained `"16": "^0.0.2"` as a broken dependency | Replaced with proper metadata and npm scripts |