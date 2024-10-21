# FastAPI APP
import uvicorn
from fastapi import FastAPI
from api.router import router as APIRouter

app = FastAPI()

# API router
app.include_router(APIRouter, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8888, reload=True)