import json
import re
from time import time
from pydantic_core.core_schema import NullableSchema
from thefuzz import fuzz, process
import os
from typing import List, Dict, Optional
from datetime import datetime


class FileManager:
    def __init__(self):
        self.band_file = "data/band_info.json"
        self.song_file = "data/song_data.json"
        self._ensure_data_files()
        self._initialize_sample_data()

    def _ensure_data_files(self):
        """确保数据文件存在，如果不存在则创建空文件"""
        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.band_file):
            with open(self.band_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

        if not os.path.exists(self.song_file):
            with open(self.song_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _initialize_sample_data(self):
        """初始化示例数据"""
        bands = self._read_bands()
        if not bands:
            # 添加示例乐队数据
            sample_bands = [
                {
                    "id": 1,
                    "name": "MyGO!!!!!",
                    "description": "迷失自我，但却向前。她们以充满情感的摇滚乐，表达年轻人的迷茫与坚定。",
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": 2,
                    "name": "Ave Mujica",
                    "description": "虚伪的假面，真实的自我。这是一个神秘且充满戏剧性的交响乐团，每个成员都带着面具。",
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": 3,
                    "name": "Poppin'Party",
                    "description": "充满活力的流行摇滚乐队，用音乐传递快乐和正能量。",
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": 4,
                    "name": "Roselia",
                    "description": "追求完美音乐表现的实力派乐队，以华丽的哥特式风格著称。",
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": 5,
                    "name": "Afterglow",
                    "description": "青梅竹马组成的硬摇滚乐队，音乐风格强烈而直接。",
                    "created_at": datetime.now().isoformat()
                }
            ]
            self._write_bands(sample_bands)

    def _read_bands(self) -> List[Dict]:
        """读取乐队数据"""
        file = open(self.band_file, mode="r")
        raw_json = file.read()
        data_obj = json.loads(raw_json)
        file.close()
        return data_obj

    def _write_bands(self, bands: List[Dict]):
        """写入乐队数据"""
        file = open(self.band_file, mode="w")
        file.write(json.dumps(bands))
        file.close()

    def _read_songs(self) -> List[Dict]:
        """读取歌曲数据"""
        file = open(self.song_file, mode="r")
        raw_json = file.read()
        data_obj = json.loads(raw_json)
        file.close()
        return data_obj

    def _write_songs(self, songs: List[Dict]):
        """写入歌曲数据"""
        file = open(self.song_file, mode="w")
        file.write(json.dumps(songs))
        file.close()

    def _generate_band_id(self) -> int:
        """生成乐队ID"""
        bands = self._read_bands()
        if not bands:
            return 1
        return max(band.get('id', 0) for band in bands) + 1

    def _generate_song_id(self) -> int:
        """生成歌曲ID"""
        songs = self._read_songs()
        if not songs:
            return 1
        return max(song.get('id', 0) for song in songs) + 1

    # 乐队相关操作
    def get_all_bands(self) -> List[Dict]:
        """获取所有乐队"""
        return self._read_bands()

    def get_band_by_name(self, name: str) -> Optional[Dict]:
        """根据名称获取乐队"""
        all_bands = self._read_bands()
        for k in all_bands:
            if k["name"] == name:
                return k
        return None

    def get_band_by_id(self, band_id: int) -> Optional[Dict]:
        """根据ID获取乐队"""
        bands = self._read_bands()
        for band in bands:
            if band.get('id') == band_id:
                return band
        return None

    def create_band(self, band_data: Dict) -> Dict:
        """创建新乐队"""
        bands = self._read_bands()

        # 检查乐队名称是否已存在
        if any(band.get('name') == band_data.get('name') for band in bands):
            raise ValueError("乐队名称已存在")

        # 生成新ID和时间戳
        band_data['id'] = self._generate_band_id()
        band_data['created_at'] = datetime.now().isoformat()

        bands.append(band_data)
        self._write_bands(bands)
        return band_data

    # 歌曲相关操作
    def get_all_songs(self) -> List[Dict]:
        """获取所有歌曲"""
        songs = self._read_songs()
        return songs

    def get_song_by_id(self, song_id: int) -> Optional[Dict]:
        """根据ID获取歌曲"""
        songs = self._read_songs()
        for song in songs:
            if song.get('id') == song_id:
                return song
        return None

    def get_songs_by_band(self, band_name: str) -> List[Dict]:
        """根据乐队获取歌曲"""
        result = []
        all_songs = self.get_all_songs()
        for i in all_songs:
            if i["band"] == band_name:
                result.append(i)
        return result

    def search_songs_by_title(self, title: str) -> List[Dict]:
        """根据标题搜索歌曲"""
        all_songs = self.get_all_songs()
        filtered = process.extract(title, all_songs)
        result = []
        for (item, score) in filtered:
            result.append(item)
        return result

    def create_song(self, song_data: Dict) -> Dict:
        """创建新歌曲"""
        # 验证乐队是否存在
        if song_data["band"] is not None:
            band = self.get_band_by_name(song_data["band"])
            if band is None:
                return {}
        # 生成新ID和时间戳
        if song_data["title"] is None:
            return {}
        new_id = self._generate_song_id()
        timestamp = datetime.now().isoformat()
        all_songs = self._read_songs()
        song_data["created_at"] = song_data["updated_at"] = timestamp
        song_data["id"] = new_id
        all_songs.append(song_data)
        self._write_songs(all_songs)
        return song_data

    def update_song(self, song_id: int, song_data: Dict) -> Optional[Dict]:
        """更新歌曲"""
        # 验证乐队是否存在
        band_name = song_data.get("band")
        if band_name is not None:
            band = self.get_band_by_name(song_data["band"])
            if band is None:
                return None
        # 更新字段
        all_songs = self.get_all_songs()
        for k in all_songs:
            if k.get("id") == song_id:
                k.update(song_data)
                # 修改更新时间
                k["updated_at"] = datetime.now().isoformat()
                self._write_songs(all_songs)
                return k
        return None

    def delete_song(self, song_id: int) -> bool:
        """删除歌曲"""
        data = self._read_songs()
        data_new = []
        found = False
        for i in data:
            if i.get("id") != song_id:
                data_new.append(i)
            else:
                found = True

        if found:
            self._write_songs(data_new)
            return True
        else:
            return False  # False表示删除失败
