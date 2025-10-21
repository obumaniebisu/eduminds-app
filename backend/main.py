from fastapi import FastAPI

app = FastAPI(title="EDUMINDS APP Backend")

@app.get("/")
def home():
    return {"message": "Welcome to EDUMINDS APP Backend!"}
