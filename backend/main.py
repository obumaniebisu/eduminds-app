from fastapi import FastAPI

app = FastAPI(title="Eduminds Backend")  # only once

# Root endpoint to test app startup
@app.get("/")
def root():
    return {"message": "Eduminds backend running"}
