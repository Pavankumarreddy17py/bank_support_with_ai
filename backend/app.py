from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import customer, fraud, transactions

app = FastAPI(title="Bank Support AI", version="0.1.0")

# CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(customer.router, prefix="/api/customer", tags=["customer"])
app.include_router(fraud.router, prefix="/api/fraud", tags=["fraud"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])


@app.get("/")
async def root():
    return {"message": "Bank Support AI backend is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
