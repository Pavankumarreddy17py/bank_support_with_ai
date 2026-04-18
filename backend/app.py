from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import customer

app = FastAPI(title="Bank Support AI")

# Allow your React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the chat route
app.include_router(customer.router, prefix="/api/customer", tags=["Customer"])

@app.get("/")
async def root():
    return {"message": "Bank Support AI Backend is running"}