from fastapi import HTTPException, status

# Very small auth stub for demonstration.
# Replace with production-ready auth (OAuth2, JWT, proper key management)

def authenticate(api_key: str):
    if api_key != "test-api-key":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    return True
