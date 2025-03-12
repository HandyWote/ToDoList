# -*- coding: utf-8 -*-
"""主界面模块

这个模块实现了ToDoList应用的主界面功能，包括日历显示、日程列表管理等核心功能。
主要包含以下功能：
- 显示日历界面，支持日期选择
- 显示和管理待办日程列表
- 支持添加新日程
- 支持标记日程完成状态
- 支持从旧版日志文件导入数据

主要类：
- Ui_mainUI: 主界面类，继承自QWidget

依赖：
- PyQt5: GUI框架
- db_manager: 数据库管理模块

作者: HandyWote
"""

import sys, os
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

from addW import Ui_addW
from db_manager import DatabaseManager, DatabaseError


class Ui_mainUI(QWidget):
    """主界面类
    
    这个类实现了ToDoList应用的主界面，管理日历显示和日程列表。
    
    属性：
        delete (int): 记录已删除的日程数量
        db (DatabaseManager): 数据库管理器实例
        aw (Ui_addW): 添加日程窗口实例
    """
    
    delete = 0
    
    def __init__(self):
        """初始化主界面
        
        - 初始化数据库连接
        - 导入旧版日志文件数据（如果存在）
        - 设置界面UI组件
        """
        super().__init__()
        try:
            # 初始化数据库管理器
            self.db = DatabaseManager()
            
            # 尝试从旧的日志文件导入数据
            if os.path.exists('Date.log'):
                imported_count, failed_lines = self.db.import_from_log('Date.log')
                if failed_lines:
                    QMessageBox.warning(self, "导入警告", f"成功导入{imported_count}条日程，{len(failed_lines)}条日程导入失败。")
                elif imported_count > 0:
                    QMessageBox.information(self, "导入成功", f"成功导入{imported_count}条日程。")
                
                # 如果成功导入了数据，备份并删除旧的日志文件
                if imported_count > 0:
                    try:
                        os.rename('Date.log', 'Date.log.bak')
                    except OSError as e:
                        QMessageBox.warning(self, "警告", f"备份旧日志文件失败：{str(e)}")
        except DatabaseError as e:
            QMessageBox.critical(self, "错误", f"数据库初始化失败：{str(e)}")
            sys.exit(1)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"程序初始化失败：{str(e)}")
            sys.exit(1)

        self.setupUi(self)
        self.aw = None  # 添加日程窗口实例

    def setupUi(self, mainUI):
        """设置主界面UI组件
        
        Args:
            mainUI: 主界面实例
        """
        mainUI.setObjectName("mainUI")
        mainUI.setMinimumSize(250, 450)
        mainUI.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setWindowIcon(QIcon('icon.ico'))
        
        # 创建主布局
        self.mainLayout = QtWidgets.QVBoxLayout(mainUI)
        self.mainLayout.setContentsMargins(15, 15, 15, 15)
        self.mainLayout.setSpacing(15)
        
        # 创建日历控件
        self.calendar = QtWidgets.QCalendarWidget(mainUI)
        self.calendar.setGridVisible(True)
        self.calendar.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        self.calendar.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendar.setNavigationBarVisible(True)
        self.calendar.setDateEditEnabled(True)
        self.calendar.setObjectName("calendar")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.calendar.setSizePolicy(sizePolicy)
        self.mainLayout.addWidget(self.calendar)
        
        # 设置日历默认选中当前日期
        now_Date = datetime.now().date()
        self.calendar.setSelectedDate(now_Date)

        # 创建日程显示区域
        self.date = QtWidgets.QGroupBox(mainUI)
        self.date.setFlat(True)
        self.date.setCheckable(False)
        self.date.setObjectName("date")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.date.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.date)
        self.verticalLayout.setContentsMargins(10, 15, 10, 10)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainLayout.addWidget(self.date)
        
        # 生成日程对应的复选框
        self.productCheckBox()

        # 创建底部布局
        bottomLayout = QtWidgets.QVBoxLayout()
        bottomLayout.setSpacing(8)
        
        # 创建添加日程按钮
        font = QtGui.QFont()
        font.setBold(True)
        self.addToDo = QtWidgets.QPushButton(mainUI)
        self.addToDo.setFont(font)
        self.addToDo.setMinimumHeight(30)
        self.addToDo.setObjectName("addToDo")
        bottomLayout.addWidget(self.addToDo)
        
        # 创建作者信息标签
        self.label = QtWidgets.QLabel(mainUI)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        bottomLayout.addWidget(self.label)
        
        self.mainLayout.addLayout(bottomLayout)

        # 设置界面样式
        self._setupStyleSheet(mainUI)

        self.retranslateUi(mainUI)
        self.addToDo.clicked.connect(self.toAddW)
        QtCore.QMetaObject.connectSlotsByName(mainUI)

    def _setupStyleSheet(self, mainUI):
        """设置界面样式表
        
        Args:
            mainUI: 主界面实例
        """
        mainUI.setStyleSheet("""
                QWidget#mainUI {
                    background: rgba(255, 255, 255, 0.85);
                    border-radius: 12px;
                    border: 1px solid rgba(200, 200, 200, 0.3);
                }
                QCalendarWidget {
                    background: rgba(245, 245, 245, 0.9);
                    border-radius: 12px;
                    border: 1px solid rgba(200, 200, 200, 0.2);
                }
                QCalendarWidget QToolButton {
                    color: #333;
                    font-size: 13px;
                    icon-size: 20px;
                }
                QCalendarWidget QMenu {
                    background: rgba(255, 255, 255, 0.95);
                    border: 1px solid rgba(200, 200, 200, 0.3);
                    border-radius: 8px;
                }
                QCalendarWidget QSpinBox {
                    background: transparent;
                    color: #333;
                    padding: 2px;
                }
                QCalendarWidget QAbstractItemView {
                    outline: 0;
                    selection-background-color: rgba(0, 122, 255, 0.6);
                    selection-color: white;
                }
                QGroupBox {
                    background: rgba(245, 245, 245, 0.8);
                    border: 1px solid rgba(200, 200, 200, 0.2);
                    border-radius: 12px;
                    margin-top: 15px;
                }
                QPushButton {
                    background: rgba(255, 255, 255, 0.9);
                    border: 1px solid rgba(200, 200, 200, 0.3);
                    border-radius: 8px;
                    padding: 6px 12px;
                    color: #333;
                }
                QPushButton:hover {
                    background: rgba(245, 245, 245, 0.9);
                }
                QCalendarWidget QWidget#qt_calendar_navigationbar {
                    background: rgba(245, 245, 245, 0.7);
                    border-radius: 8px;
                    padding: 4px;
                }
                QCalendarWidget QToolButton::menu-indicator {
                    image: none;
                }
                QCalendarWidget QTableView {
                    alternate-background-color: transparent;
                    gridline-color: rgba(200, 200, 200, 0.2);
                }
                QCalendarWidget QTableView::item {
                    border: none;
                    padding: 4px;
                }
                QCalendarWidget QTableView::item:selected {
                    border-radius: 4px;
                }
            """)

    def retranslateUi(self, mainUI):
        """设置UI组件的文本内容
        
        Args:
            mainUI: 主界面实例
        """
        _translate = QtCore.QCoreApplication.translate
        mainUI.setWindowTitle(_translate("mainUI", "ToDoList"))
        self.date.setTitle(_translate("mainUI", "日程："))
        self.addToDo.setText(_translate("mainUI", "添加日程"))
        self.label.setText(_translate("mainUI", "<a href='https://github.com/HandyWote/ToDoList'>作者:HandyWote</a>"))

    def toAddW(self):
        """显示添加日程窗口
        
        创建并显示添加日程窗口，同时连接信号用于刷新主界面的日程列表。
        """
        self.aw = Ui_addW()  # 创建添加日程窗口实例
        self.aw.signal.connect(self.refreshCheckboxes)  # 连接信号到刷新方法
        self.aw.show()  # 显示窗口

    def refreshCheckboxes(self):
        """刷新日程列表
        
        清空并重新加载所有日程对应的复选框。
        """
        self.delete = 0
        # 清空现有的复选框
        while self.verticalLayout.count():
            item = self.verticalLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        # 重新生成复选框
        self.productCheckBox()

    def productCheckBox(self):
        """生成日程对应的复选框
        
        从数据库获取未完成的日程，并为每个日程创建对应的复选框。
        """
        try:
            todos = self.db.get_uncompleted_todos()
            for todo_id, datetime_str, content in todos:
                checkbox = QtWidgets.QCheckBox(f"{datetime_str}\t{content}")
                checkbox.setProperty("todo_id", todo_id)
                self.verticalLayout.addWidget(checkbox)
                checkbox.stateChanged.connect(self.checkboxStatusChanged)
        except DatabaseError as e:
            QMessageBox.warning(self, "错误", f"获取日程失败：{str(e)}")

    def checkboxStatusChanged(self):
        """处理复选框状态变化
        
        当用户勾选复选框时，将对应的日程标记为已完成。
        """
        checkbox = self.sender()
        if checkbox:
            todo_id = checkbox.property("todo_id")
            try:
                if self.db.mark_todo_completed(todo_id):
                    self.delete += 1
                else:
                    QMessageBox.warning(self, "错误", "更新日程状态失败")
            except DatabaseError as e:
                QMessageBox.warning(self, "错误", f"标记日程完成失败：{str(e)}")
                checkbox.setChecked(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Dlg = Ui_mainUI()
    Dlg.show()
    sys.exit(app.exec_())
