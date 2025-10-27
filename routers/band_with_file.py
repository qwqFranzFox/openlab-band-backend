from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, List
from services.file_manager import FileManager
from models.bangdream_models import (
    BandResponse, SongCreate, SongResponse, SongUpdate, PaginatedResponse
)

router = APIRouter(prefix="/api", tags=["文件存储版本"])
file_manager = FileManager()

@router.get("/bands", response_model=List[BandResponse])
def get_bands(name: Optional[str] = Query(None, description="乐队名称")):
    """获取乐队列表或根据名称查询特定乐队"""
    """TODO:通过调用service层的对应函数，实现按name查询乐队功能的接口"""

@router.get("/songs", response_model=PaginatedResponse)
def get_songs(
    band: Optional[str] = Query(None, description="乐队名称"),
    title: Optional[str] = Query(None, description="歌曲名称（模糊搜索）"),
    page_index: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量")
):
    """获取歌曲列表，支持按乐队、标题搜索和分页"""
    """TODO:通过调用service层的对应函数，实现按乐队、标题过滤和分页获取歌曲列表的接口"""

@router.get("/songs/{song_id}", response_model=SongResponse)
def get_song_detail(song_id: int = Path(..., ge=1, description="歌曲ID")):
    """根据ID获取歌曲详情"""
    """TODO:通过调用service层的对应函数，实现根据ID获取歌曲详情的接口"""

@router.post("/songs", response_model=SongResponse, status_code=201)
def create_song(song: SongCreate):
    """创建新歌曲"""
    """TODO:通过调用service层的对应函数，实现创建新歌曲的接口"""

@router.put("/songs/{song_id}", response_model=SongResponse)
def update_song(song_id: int = Path(..., ge=1, description="歌曲ID"), song: SongUpdate = None):
    """更新歌曲信息"""
    """TODO:通过调用service层的对应函数，实现更新歌曲信息的接口"""

@router.delete("/songs/{song_id}", status_code=204)
def delete_song(song_id: int = Path(..., ge=1, description="歌曲ID")):
    """删除歌曲"""
    """TODO:通过调用service层的对应函数，实现删除歌曲的接口"""