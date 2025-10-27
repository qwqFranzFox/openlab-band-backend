from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Pydantic模型（用于请求/响应验证）
class BandBase(BaseModel):
    name: str
    description: str

class BandCreate(BandBase):
    pass

class BandResponse(BandBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SongBase(BaseModel):
    title: str
    author: Optional[str] = None
    lyrics: Optional[str] = None
    band: str

class SongCreate(SongBase):
    pass

class SongUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    lyrics: Optional[str] = None
    band: Optional[str] = None

class SongResponse(SongBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    songs: List[SongResponse]
    total: int
    page_index: int
    page_size: int