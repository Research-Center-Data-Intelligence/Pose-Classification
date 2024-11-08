from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from tempfile import NamedTemporaryFile
from lstm import api_prediction
import io
import joblib
import numpy as np
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def convert_keypoints_to_json(keypoints):
    return [kp.tolist() if isinstance(kp, np.ndarray) else kp for kp in keypoints]


@app.post("/keypoints")
async def upload_file(file: UploadFile = File(...)):
    try:
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
        tracking_results = joblib.load(temp_file_path)
        keypoints_data = tracking_results[0]["keypoints"]
        json_keypoints = convert_keypoints_to_json(keypoints_data)
        os.remove(temp_file_path)
        return {"keypoints": json_keypoints}
    except Exception as e:
        return {"error": str(e)}


@app.post("/predict")
async def predict(file: UploadFile = File(...), architecture: str = Form(...)):
    file_content = file.file.read()
    prediction = api_prediction(io.BytesIO(file_content))
    print(architecture)
    return {"prediction": prediction}
