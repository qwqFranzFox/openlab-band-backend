import sqlite3
import os
from typing import List, Optional, Tuple, Dict, Any, clear_overloads, final
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
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bands WHERE name = '"+(name)+"'")
            row = cursor.fetchone()
            if row is not None:
                return self.row_to_dict(row)
            else:
                return None
        finally:
            conn.close()

            # 歌曲相关操作
    def get_songs(
        self,
        band: Optional[str] = None,
        title: Optional[str] = None,
        page_index: int = 1,
        page_size: int = 10
    ) -> Tuple[List[Dict[str, Any]], int]:
        """获取歌曲列表（支持分页和过滤）"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            if band is not None:
                cursor.execute(
                    "SELECT * FROM songs WHERE band = '" + band+"'")
            elif title is not None:
                cursor.execute(
                    "SELECT * FROM songs WHERE title = '"+title+"'")
            else:
                cursor.execute("SELECT * FROM songs ORDER BY id")
            data = cursor.fetchall()
            res = []
            for i in range((page_index-1)*page_size, min(len(data), (page_index)*page_size)):
                res.append(data[i])
            return [self.row_to_dict(row) for row in res], len(data)
            # return [self.row_to_dict(row) for row in data], len(data)
        except Exception as e:
            conn.close()
            raise e
        finally:
            conn.close()
            # return ([], 0)

    def get_song_by_id(self, song_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取歌曲"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM songs WHERE id = "+str(song_id))
            rows = cursor.fetchone()
            return self.row_to_dict(rows)
        finally:
            conn.close()

    def create_song(self, song_data: dict) -> int:
        """创建新歌曲"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO songs (title,author,lyrics,band,created_at,updated_at) VALUES (?,?,?,?,?,?)", (song_data["title"], song_data[
                           "author"], song_data["lyrics"], song_data["band"], datetime.now().isoformat(), datetime.now().isoformat()))
            conn.commit()
            cursor.execute("SELECT last_insert_rowid()")
            res = cursor.fetchone()[0]
            conn.close()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def update_song(self, song_id: int, song_data: dict) -> bool:
        """更新歌曲信息"""
        song = self.get_song_by_id(song_id)
        if song is None:
            return False
        conn = self.get_connection()
        try:
            if song_data.get("title") is not None:
                conn.execute("UPDATE songs SET title=? WHERE id = ?",
                             (song_data["title"], song_id))
            if song_data.get("author") is not None:
                conn.execute("UPDATE songs SET author=? WHERE id = ?",
                             (song_data["author"], song_id))
            if song_data.get("lyrics") is not None:
                conn.execute("UPDATE songs SET lyrics=? WHERE id = ?",
                             (song_data["lyrics"], song_id))
            if song_data.get("band") is not None:
                conn.execute("UPDATE songs SET band=? WHERE id = ?",
                             (song_data["band"], song_id))
            conn.execute("UPDATE songs SET updated_at=? WHERE id = ?",
                         (datetime.now().isoformat(), song_id))
            assert conn.total_changes > 0
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
            return False
        finally:
            conn.close()

    def delete_song(self, song_id: int) -> bool:
        """删除歌曲"""
        song = self.get_song_by_id(song_id)
        if song is None:
            return False
        conn = self.get_connection()
        try:
            conn.execute("DELETE FROM songs WHERE id = "+str(song_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
            return False
        finally:
            conn.close()
            return True  # False表示删除失败
