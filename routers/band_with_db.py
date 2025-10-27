from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from models.bangdream_models import (
    BandResponse, SongCreate, SongResponse, SongUpdate, PaginatedResponse
)
from services.db_manager import DatabaseManager

router = APIRouter(prefix="/api", tags=["bands"])
db_manager = DatabaseManager()

@router.get("/bands", response_model=List[BandResponse])
def get_bands(name: Optional[str] = Query(None)):
    """获取所有乐队或按名称查询特定乐队"""
    """TODO:通过调用service层的对应函数，实现按name查询乐队功能的接口"""

@router.get("/songs", response_model=PaginatedResponse)
def get_songs(
    band: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    page_index: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """获取歌曲列表（支持分页和过滤）"""
    """TODO:通过调用service层的对应函数，实现按乐队、标题过滤和分页获取歌曲列表的接口"""

@router.get("/songs/{song_id}", response_model=SongResponse)
def get_song(song_id: int):
    """根据ID获取歌曲详情"""
    song = db_manager.get_song_by_id(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="歌曲不存在")
    return song

@router.post("/songs", response_model=SongResponse, status_code=201)
def create_song(song: SongCreate):
    """创建新歌曲"""
    """TODO:通过调用service层的对应函数，实现创建新歌曲的接口"""

@router.put("/songs/{song_id}", response_model=SongResponse)
def update_song(song_id: int, song: SongUpdate):
    """更新歌曲信息"""
    """TODO:通过调用service层的对应函数，实现更新歌曲信息的接口"""


@router.delete("/songs/{song_id}", status_code=204)
def delete_song(song_id: int):
    """删除歌曲"""
    """TODO:通过调用service层的对应函数，实现删除歌曲的接口"""