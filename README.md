
# ToDoList

一个基于PyQt5的待办事项管理应用。

## 功能特点

- 日历界面显示，支持日期选择
- 待办事项管理（添加、标记完成）
- 美观的现代化UI界面
- 数据持久化存储
- 支持从旧版日志文件导入数据

## 技术栈

- Python 3.x
- PyQt5：GUI框架
- SQLite：数据存储

## 项目结构

```
├── mainUI.py      # 主界面实现
├── addW.py        # 添加日程窗口实现
├── db_manager.py  # 数据库管理模块
├── API.md         # API文档
├── icon.ico       # 应用图标
└── UI/            # UI设计文件
    ├── mainUI.ui
    └── addW.ui
```

## 数据存储

应用使用SQLite数据库存储待办事项，数据文件为`todo.db`。同时支持从旧版的`Date.log`文件导入数据。

## 错误处理

应用实现了完整的错误处理机制：
- 数据库操作异常处理
- 文件导入异常处理
- 用户输入验证

## UI设计

- 现代化的半透明界面设计
- 圆角边框和阴影效果
- 响应式布局，支持窗口大小调整
- 统一的颜色主题

## 开发者

- HandyWote
- GitHub: https://github.com/HandyWote/ToDoList

## 许可证

MIT License
