from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from logging import log

from models.bangdream_models import (
    BandResponse, SongCreate, SongResponse, SongUpdate, PaginatedResponse
)
from services.db_manager import DatabaseManager

router = APIRouter(prefix="/api", tags=["bands"])
db_manager = DatabaseManager()


@router.get("/bands", response_model=List[BandResponse])
def get_bands(name: Optional[str] = Query(None)):
    """获取所有乐队或按名称查询特定乐队"""
    res = []
    if name is not None:
        res = db_manager.get_band_by_name(name=name)
        if res is not None:
            return [BandResponse(**res)]
        else:
            raise HTTPException(status_code=404, detail="乐队不存在")
    else:
        res = db_manager.get_all_bands()
        if res is not None:
            return [BandResponse(**item) for item in res]
            # log(msg=str(res), level=1)
        else:
            raise HTTPException(status_code=404, detail="乐队不存在")


@router.get("/songs", response_model=PaginatedResponse)
def get_songs(
    band: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    page_index: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """获取歌曲列表（支持分页和过滤）"""
    res = db_manager.get_songs(band, title, page_index, page_size)
    if res is not None:
        content, size = res
        return PaginatedResponse(songs=[SongResponse(**cont) for cont in content], page_size=page_size, page_index=page_index, total=size)
    else:
        raise HTTPException(status_code=404, detail="乐队不存在")


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
    res = db_manager.create_song(song.model_dump())
    if res != 0:  # Success
        band = db_manager.get_song_by_id(res)
        if band is not None:
            return SongResponse(**band)
        else:
            raise HTTPException(status_code=404, detail="歌曲不存在")
    else:
        raise HTTPException(status_code=400, detail="请求格式错误")


@router.put("/songs/{song_id}", response_model=SongResponse)
def update_song(song_id: int, song: SongUpdate):
    """更新歌曲信息"""
    res = db_manager.update_song(song_id, song.model_dump())
    if res != 0:
        song_data = db_manager.get_song_by_id(song_id)
        if song_data is not None:
            return SongResponse(**song_data)
        raise HTTPException(status_code=404, detail="歌曲不存在")


@router.delete("/songs/{song_id}", status_code=204)
def delete_song(song_id: int):
    """删除歌曲"""
    res = db_manager.delete_song(song_id)
    if not res:
        raise HTTPException(status_code=404, detail="歌曲不存在")
