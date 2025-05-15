from fastapi import FastAPI

from src.receipts.router import router as receipts_router
from src.users.router import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(receipts_router)


@app.get("/")
def root():
    return {"message": "RUNNING"}
