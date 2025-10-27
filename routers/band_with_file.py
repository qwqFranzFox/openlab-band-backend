from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, List
from services.file_manager import FileManager
from models.bangdream_models import (
    BandResponse, SongCreate, SongResponse, SongUpdate, PaginatedResponse
)
import json

router = APIRouter(prefix="/api", tags=["文件存储版本"])
file_manager = FileManager()


@router.get("/bands", response_model=List[BandResponse])
def get_bands(name: Optional[str] = Query(None, description="乐队名称")):
    """获取乐队列表或根据名称查询特定乐队"""
    if name is None:
        # Get List
        all_bands = file_manager.get_all_bands()
        result = []
        for k in all_bands:
            resp = BandResponse(**k)
            result.append(resp)
        return result
    else:
        some_band = file_manager.get_band_by_name(name)
        if some_band is None:
            raise HTTPException(status_code=404, detail="乐队不存在")
        return [BandResponse(**some_band)]


@router.get("/songs", response_model=PaginatedResponse)
def get_songs(
    band: Optional[str] = Query(None, description="乐队名称"),
    title: Optional[str] = Query(None, description="歌曲名称（模糊搜索）"),
    page_index: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量")
):
    """获取歌曲列表，支持按乐队、标题搜索和分页"""
    songs = []
    if band is not None:
        # has band
        songs = file_manager.get_songs_by_band(band)
    elif title is not None:
        # has title
        songs = file_manager.search_songs_by_title(title)
    else:
        # get all by page
        songs = file_manager.get_all_songs()

    tran = []
    for k in songs:
        tran.append(SongResponse(**k))

    result = []
    if (page_index-1)*page_size > len(tran):
        raise HTTPException(status_code=400, detail="请求参数错误")
    for i in range((page_index-1)*page_size, min(page_index*page_size, len(tran)), 1):
        result.append(tran[i])

    return PaginatedResponse(songs=result, page_index=page_index, page_size=page_size, total=len(tran))


@router.get("/songs/{song_id}", response_model=SongResponse)
def get_song_detail(song_id: int = Path(..., ge=1, description="歌曲ID")):
    """根据ID获取歌曲详情"""
    song = file_manager.get_song_by_id(song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="歌曲不存在")
    else:
        return SongResponse(**song)


@router.post("/songs", response_model=SongResponse, status_code=201)
def create_song(song: SongCreate):
    """创建新歌曲"""
    res = file_manager.create_song(dict(song))
    if res == {}:
        raise HTTPException(status_code=400, detail="请求参数错误")
    return SongResponse(**res)


@router.put("/songs/{song_id}", response_model=SongResponse)
def update_song(song_id: int = Path(..., ge=1, description="歌曲ID"), song: SongUpdate = None):
    """更新歌曲信息"""
    res = file_manager.update_song(song_id, dict(song))
    if res is not None:
        return SongResponse(**res)
    raise HTTPException(status_code=404, detail="歌曲不存在")


@router.delete("/songs/{song_id}", status_code=204)
def delete_song(song_id: int = Path(..., ge=1, description="歌曲ID")):
    """删除歌曲"""
    if not file_manager.delete_song(song_id):
        raise HTTPException(status_code=404, detail="歌曲不存在")
