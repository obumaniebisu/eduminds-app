from fastapi import FastAPI, Request
import json
import base64

app = FastAPI()  # only once

# Root endpoint
@app.get("/")
def root():
    return {"message": "Eduminds backend running"}

# Endpoint to get logged-in user info
@app.get("/me")
async def get_user(request: Request):
    # Azure AD passes user info in X-MS-CLIENT-PRINCIPAL header
    encoded_header = request.headers.get("X-MS-CLIENT-PRINCIPAL")
    if not encoded_header:
        return {"error": "No user info found"}

    decoded_bytes = base64.b64decode(encoded_header)
    decoded_str = decoded_bytes.decode("utf-8")
    user_info = json.loads(decoded_str)

    return {"user": user_info}

# Only needed for local testing with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
