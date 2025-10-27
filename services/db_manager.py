import sqlite3
import os
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path: str = "data/band.db"):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 使查询结果可以像字典一样访问
        return conn

    def init_database(self):
        """初始化数据库表结构"""
        # 确保数据目录存在
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # 创建乐队表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建歌曲表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS songs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT,
                    lyrics TEXT,
                    band TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 插入初始乐队数据
            initial_bands = [
                ("MyGO!!!!!", "迷失自我，但却向前。她们以充满情感的摇滚乐，表达年轻人的迷茫与坚定。"),
                ("Ave Mujica", "虚伪的假面，真实的自我。这是一个神秘且充满戏剧性的交响乐团，每个成员都带着面具。"),
                ("Morfonica", "如梦似幻的交响乐团。她们以小提琴为主轴，演奏出优雅而华丽的乐章。")
            ]
            
            cursor.executemany(
                "INSERT OR IGNORE INTO bands (name, description) VALUES (?, ?)",
                initial_bands
            )
            # 检查歌曲表是否为空
            cursor.execute("SELECT COUNT(*) as count FROM songs")
            song_count = cursor.fetchone()["count"]

            if song_count == 0:
            # 插入一些示例歌曲数据
                initial_songs = [
                    ("黑色生日", "Doloris", "歌词内容...", "Ave Mujica"),
                    ("迷星叫", "MyGO!!!!!", "歌词内容...", "MyGO!!!!!")
                ]
                
                cursor.executemany(
                    "INSERT OR IGNORE INTO songs (title, author, lyrics, band) VALUES (?, ?, ?, ?)",
                    initial_songs
                )
            
            conn.commit()
        finally:
            conn.close()

    def row_to_dict(self, row) -> Dict[str, Any]:
        """将sqlite3.Row转换为字典"""
        if row is None:
            return None
        return dict(row)

    # 乐队相关操作
    def get_all_bands(self) -> List[Dict[str, Any]]:
        """获取所有乐队"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bands ORDER BY name")
            rows = cursor.fetchall()
            return [self.row_to_dict(row) for row in rows]
        finally:
            conn.close()

    def get_band_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """根据名称获取乐队"""
        """TODO:根据name，从数据库中获取乐队数据"""

    # 歌曲相关操作
    def get_songs(
        self, 
        band: Optional[str] = None,
        title: Optional[str] = None,
        page_index: int = 1,
        page_size: int = 10
    ) -> Tuple[List[Dict[str, Any]], int]:
        """获取歌曲列表（支持分页和过滤）"""
        """TODO:从数据库中获取歌曲列表，支持按乐队、标题过滤和分页"""

    def get_song_by_id(self, song_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取歌曲"""
        """TODO:根据song_id，从数据库中获取歌曲数据"""

    def create_song(self, song_data: dict) -> int:
        """创建新歌曲"""
        """TODO:将新歌曲数据插入数据库，返回新创建的歌曲ID"""

    def update_song(self, song_id: int, song_data: dict) -> bool:
        """更新歌曲信息"""
        """TODO:更新指定ID的歌曲信息，返回是否成功"""

    def delete_song(self, song_id: int) -> bool:
        """删除歌曲"""
        """TODO:删除指定ID的歌曲，返回是否成功"""
        return False # False表示删除失败