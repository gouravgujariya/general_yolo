from fastapi import FastAPI, HTTPException
import ultralytics
import requests
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Define the request structure using pydantic
class ModelRequest(BaseModel):
    model_name: str
    task: str
    data_link: str
    epochs: int
    export_format: str

# Define the response model
class ModelResponse(BaseModel):
    model_export_path: str
    result_file: str
    message: str

# task based model selection
def select_model(model_name: str, task: str) -> str:
    match task:
        case "segment":
            return "yolov8n-seg"
        case "classify":
            return "yolov8n-cls"
        case "pose":
            return "yolov8n-pose"
        case "obb":
            return "yolov8-obb"
        case _:
            raise HTTPException(status_code=400, detail="Invalid task")

# Define a function to download data from a URL
def download_data(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download data.")
    with open("data.yaml", "wb") as f:
        f.write(response.content)
    return "data.yaml"

# Define a function to train a YOLO model
def train_model(model_name: str, data: str, epochs: int) -> ultralytics.YOLO:
    model = ultralytics.YOLO(model_name)
    model.train(data, epochs=epochs)
    return model

# Define a function to export a YOLO model
def export_model(model: ultralytics.YOLO, export_format: str, model_name: str) -> str:
    model.export(format=export_format)
    return f"{model_name}.{export_format}"

@app.post("/train_model/")
async def train_model_endpoint(request: ModelRequest):
    try:
        # Select model based on task
        model_name = select_model(request.model_name, request.task)

        # Download data
        data = download_data(request.data_link)

        # Train model
        model = train_model(model_name, data, request.epochs)

        # Export model
        model_export_path = export_model(model, request.export_format, model_name)

        # Return response
        return ModelResponse(
            model_export_path=model_export_path,
            result_file="results.txt",  # Replace with actual result file
            message="Model trained and exported successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)