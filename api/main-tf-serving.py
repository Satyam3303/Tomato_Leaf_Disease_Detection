from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import requests

app = FastAPI(title="Tomato Leaf Disease Detection API (TF Serving)")

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TF_SERVING_HOST = "localhost"
TF_SERVING_PORT = 8501
MODEL_NAME = "tomatoes_model"  # FIX: was "potatoes_model"
endpoint = f"http://{TF_SERVING_HOST}:{TF_SERVING_PORT}/v1/models/{MODEL_NAME}:predict"

CLASS_NAMES = [
    "Bacterial_spot",
    "Early_blight",
    "Late_blight",
    "Leaf_Mold",
    "Septoria_leaf_spot",
    "Spider_mites",
    "Target_Spot",
    "Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato_mosaic_virus",
    "healthy",
]


@app.get("/ping")
async def ping():
    return {"status": "alive", "message": "Tomato Disease Detection API (TF Serving) is running"}


def read_file_as_image(data: bytes) -> np.ndarray:
    image = Image.open(BytesIO(data)).convert("RGB")
    image = image.resize((256, 256))
    return np.array(image)


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, axis=0)

    json_data = {"instances": img_batch.tolist()}

    try:
        response = requests.post(endpoint, json=json_data, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to TF Serving at {endpoint}.",
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"TF Serving error: {str(e)}")

    prediction = np.array(response.json()["predictions"][0])
    predicted_class = CLASS_NAMES[np.argmax(prediction)]
    confidence = float(np.max(prediction))

    return {
        "class": predicted_class,
        "confidence": confidence,
        "confidence_percent": f"{confidence * 100:.2f}%",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)