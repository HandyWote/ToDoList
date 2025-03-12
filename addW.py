# -*- coding: utf-8 -*-
"""添加日程窗口模块

这个模块实现了ToDoList应用的添加日程功能，提供了一个独立的窗口用于输入新日程。
主要包含以下功能：
- 日期时间选择
- 日程内容输入
- 保存日程到数据库

主要类：
- Ui_addW: 添加日程窗口类，继承自QWidget

依赖：
- PyQt5: GUI框架
- db_manager: 数据库管理模块

作者: HandyWote
"""

from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox
from db_manager import DatabaseManager, DatabaseError


class Ui_addW(QWidget):
    """添加日程窗口类
    
    这个类实现了添加日程的窗口界面，包括日期时间选择器和日程内容输入框。
    
    属性：
        signal (pyqtSignal): 用于在保存日程后通知主窗口刷新列表的信号
        db (DatabaseManager): 数据库管理器实例
    """
    
    signal = QtCore.pyqtSignal()  # 创建信号对象

    def __init__(self, parent=None):
        """初始化添加日程窗口
        
        Args:
            parent: 父窗口实例，默认为None
        """
        super().__init__(parent)
        self.setWindowIcon(QIcon('icon.ico'))  # 设置窗口图标
        try:
            self.db = DatabaseManager()
        except DatabaseError as e:
            QMessageBox.critical(self, "错误", f"数据库初始化失败：{str(e)}")
            self.close()
            return
        self.setupUi(self)  # 初始化UI组件

    def setupUi(self, addW):
        """设置窗口UI组件
        
        Args:
            addW: 窗口实例
        """
        addW.setObjectName("addW")  # 设置窗口对象名称
        addW.setMinimumSize(250, 350)  # 设置最小窗口大小，与主窗口保持相同宽度，高度适中
        self.setWindowIcon(QIcon('icon.ico'))  # 设置窗口图标

        # 创建主布局
        self.mainLayout = QtWidgets.QVBoxLayout(addW)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(15)

        # 创建并设置日期时间编辑框
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(addW)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.dateTimeEdit.setFont(font)
        self.dateTimeEdit.setAlignment(QtCore.Qt.AlignCenter)
        now = datetime.now()
        self.dateTimeEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(now.year, now.month, now.day), QtCore.QTime(now.hour, now.minute, now.second)))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.dateTimeEdit.setSizePolicy(sizePolicy)
        self.mainLayout.addWidget(self.dateTimeEdit)

        # 创建并设置文本编辑框
        self.textEdit = QtWidgets.QTextEdit(addW)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.textEdit.setSizePolicy(sizePolicy)
        self.mainLayout.addWidget(self.textEdit)

        # 创建并设置保存按钮
        self.save = QtWidgets.QPushButton(addW)
        self.save.setFont(font)
        self.save.setObjectName("save")
        self.save.setMinimumHeight(40)
        self.mainLayout.addWidget(self.save)

        # 设置窗口样式
        addW.setStyleSheet("""
                QWidget#addW {
                    background: rgba(255, 255, 255, 0.85);
                    border-radius: 12px;
                    border: 1px solid rgba(200, 200, 200, 0.3);
                }
                QDateTimeEdit, QTextEdit {
                    background: rgba(255, 255, 255, 0.8);
                    border: 1px solid rgba(200, 200, 200, 0.3);
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton {
                    background: rgba(255, 255, 255, 0.9);
                    border: 1px solid rgba(200, 200, 200, 0.3);
                    border-radius: 8px;
                    padding: 8px;
                    color: #333;
                }
                QPushButton:hover {
                    background: rgba(245, 245, 245, 0.9);
                }
            """)

        self.retranslateUi(addW)  # 设置UI元素的文本内容
        self.save.clicked.connect(self.saveBM)  # 连接保存按钮的点击事件到saveBM方法
        QtCore.QMetaObject.connectSlotsByName(addW)  # 根据名称自动连接所有槽函数

    def retranslateUi(self, addW):
        """设置UI组件的文本内容
        
        Args:
            addW: 窗口实例
        """
        _translate = QtCore.QCoreApplication.translate
        addW.setWindowTitle(_translate("addW", "添加日程"))  # 设置窗口标题为"添加日程"
        self.textEdit.setPlaceholderText(_translate("addW", "请输入日程："))  # 设置文本编辑框的占位符文本
        self.save.setText(_translate("addW", "保存"))  # 设置保存按钮的文本为"保存"

    def saveBM(self):
        """保存日程
        
        获取用户输入的日期时间和日程内容，验证后保存到数据库。
        成功保存后发送信号通知主窗口刷新，并关闭添加窗口。
        """
        try:
            todo_text = self.textEdit.toPlainText().strip()
            time_text = self.dateTimeEdit.text()
            
            if not todo_text:
                QMessageBox.warning(self, "提示", "请输入日程内容")
                return
                
            if self.db.add_todo(time_text, todo_text):
                self.signal.emit()
                self.close()
            else:
                QMessageBox.warning(self, "错误", "保存日程失败")
        except DatabaseError as e:
            QMessageBox.warning(self, "错误", f"保存日程失败：{str(e)}")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"发生未知错误：{str(e)}")