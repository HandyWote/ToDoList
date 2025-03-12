# ToDoList API 文档

## 项目概述

ToDoList是一个基于PyQt5的日程管理应用，提供日历视图和日程管理功能。

## 模块结构

### mainUI.py
主界面模块，实现了应用的核心功能。

#### 类：Ui_mainUI
继承自QWidget，实现主界面功能。

主要方法：
- `__init__()`: 初始化主界面，包括数据库连接和UI组件设置
- `setupUi(mainUI)`: 设置UI组件和布局
- `productCheckBox()`: 生成日程对应的复选框
- `refreshCheckboxes()`: 刷新日程列表
- `checkboxStatusChanged()`: 处理复选框状态变化，标记日程完成
- `toAddW()`: 显示添加日程窗口

### addW.py
添加日程窗口模块，提供新日程的输入界面。

#### 类：Ui_addW
继承自QWidget，实现添加日程窗口功能。

主要方法：
- `__init__(parent=None)`: 初始化添加日程窗口
- `setupUi(addW)`: 设置UI组件和布局
- `saveBM()`: 保存日程到数据库

### db_manager.py
数据库管理模块，处理所有数据库操作。

#### 类：DatabaseManager
数据库管理器，提供数据库操作接口。

主要方法：
- `add_todo(time_text, todo_text)`: 添加新日程
- `get_uncompleted_todos()`: 获取未完成的日程
- `mark_todo_completed(todo_id)`: 标记日程为已完成
- `import_from_log(log_file)`: 从旧版日志文件导入数据

#### 异常：DatabaseError
自定义异常类，用于处理数据库操作相关的错误。

## 类之间的关系

1. Ui_mainUI 使用 Ui_addW 创建添加日程窗口
2. Ui_mainUI 和 Ui_addW 都使用 DatabaseManager 进行数据库操作
3. 通过Qt信号机制，Ui_addW 在保存日程后通知 Ui_mainUI 刷新日程列表

## 主要接口使用说明

### 1. 添加新日程
```python
from addW import Ui_addW

# 创建添加日程窗口
aw = Ui_addW()
# 连接信号用于刷新主界面
aw.signal.connect(refresh_callback)
# 显示窗口
aw.show()
```

### 2. 获取未完成日程
```python
from db_manager import DatabaseManager

db = DatabaseManager()
todos = db.get_uncompleted_todos()
for todo_id, datetime_str, content in todos:
    # 处理每条日程
    print(f"{datetime_str}: {content}")
```

### 3. 标记日程完成
```python
from db_manager import DatabaseManager

db = DatabaseManager()
if db.mark_todo_completed(todo_id):
    print("日程已标记为完成")
```

### 4. 从旧版日志导入数据
```python
from db_manager import DatabaseManager

db = DatabaseManager()
imported_count, failed_lines = db.import_from_log('Date.log')
print(f"成功导入{imported_count}条日程")
```

## 异常处理

所有数据库操作都可能抛出 DatabaseError 异常，建议使用 try-except 进行捕获：

```python
from db_manager import DatabaseManager, DatabaseError

try:
    db = DatabaseManager()
    db.add_todo(time_text, todo_text)
except DatabaseError as e:
    print(f"数据库操作失败：{str(e)}")
```

## UI定制

界面样式通过Qt样式表（QSS）定制，主要包括：
- 半透明背景
- 圆角边框
- 悬停效果
- 统一的颜色主题

可以通过修改 mainUI.py 和 addW.py 中的 setStyleSheet 方法来自定义界面样式。