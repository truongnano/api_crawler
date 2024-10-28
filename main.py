# FastAPI APP
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import router as APIRouter

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc chỉ định các domain cần cho phép
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# API router
app.include_router(APIRouter, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8888, reload=True)