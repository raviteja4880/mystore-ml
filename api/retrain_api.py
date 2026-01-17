from fastapi import FastAPI
import subprocess

app = FastAPI(title="ML Retraining Service")

@app.post("/retrain")
def retrain_model():
    try:
        subprocess.Popen(
            ["python", "model/train_model.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return {"status": "retraining started"}
    except Exception as e:
        return {"error": str(e)}
