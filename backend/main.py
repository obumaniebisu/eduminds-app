from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Eduminds backend running"}

# This must be at the top level, not indented under a function
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
