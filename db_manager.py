import os
import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional

class DatabaseManager:
    def __init__(self, db_path: str = 'todo.db'):
        self.db_path = db_path
        self._init_database()

    def _init_database(self) -> None:
        """初始化数据库，创建必要的表"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # 创建待办事项表
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datetime TEXT NOT NULL,
                    content TEXT NOT NULL,
                    completed INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """)
                conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"初始化数据库失败：{str(e)}")
        except Exception as e:
            raise DatabaseError(f"发生未知错误：{str(e)}")

    def add_todo(self, datetime_str: str, content: str) -> bool:
        """添加新的待办事项"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO todos (datetime, content) VALUES (?, ?)",
                    (datetime_str, content)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            raise DatabaseError(f"添加待办事项失败：{str(e)}")

    def get_uncompleted_todos(self) -> List[Tuple[int, str, str]]:
        """获取所有未完成的待办事项"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, datetime, content FROM todos WHERE completed = 0 ORDER BY datetime"
                )
                return cursor.fetchall()
        except sqlite3.Error as e:
            raise DatabaseError(f"获取待办事项失败：{str(e)}")

    def mark_todo_completed(self, todo_id: int) -> bool:
        """将待办事项标记为已完成"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE todos SET completed = 1 WHERE id = ?",
                    (todo_id,)
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            raise DatabaseError(f"更新待办事项状态失败：{str(e)}")

    def import_from_log(self, log_path: str) -> Tuple[int, List[str]]:
        """从旧的日志文件导入数据"""
        imported_count = 0
        failed_lines = []

        if not os.path.exists(log_path):
            raise FileNotFoundError(f"日志文件 {log_path} 不存在")

        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line[0] == 'Y':
                        continue
                    
                    try:
                        datetime_str, content = line.split('\t', 1)
                        self.add_todo(datetime_str, content)
                        imported_count += 1
                    except ValueError:
                        failed_lines.append(line)
                    except DatabaseError:
                        failed_lines.append(line)

            return imported_count, failed_lines
        except Exception as e:
            raise IOError(f"导入数据失败：{str(e)}")

class DatabaseError(Exception):
    """数据库操作异常"""
    pass