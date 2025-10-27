from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# 决定使用文件存储版本还是数据库版本
USE_FILE_STORAGE = True

app = FastAPI(
    title="BanG Dream! 乐队管理系统",
    description="基于FastAPI的乐队和歌曲管理API" + ("（文件存储版本）" if USE_FILE_STORAGE else "（数据库版本）"),
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根据配置注册不同的路由
if USE_FILE_STORAGE:
    from routers.band_with_file import router as band_router
    print("使用文件存储版本")
else:
    from routers.band_with_db import router as band_router
    print("使用数据库版本")

app.include_router(band_router)

@app.get("/")
async def root():
    return {"message": "BanG Dream! 乐队管理系统API", "storage_type": "file" if USE_FILE_STORAGE else "database"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)