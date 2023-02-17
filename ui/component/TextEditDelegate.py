# 使用自定义委托，一般自定义一个继承自PySide6.QtWidgets.QStyledItemDelegate的类，同时必须实现以下三个方法：

# 1.createEditor(self,parent,option,index) 用于创建数据编辑界面所用的部件（文本框、下拉列表框等）

# 2.setEditorData(self,editor,index)  用于从模型获取编辑前的原数据，并加载至编辑部件

# 3.setModelData(self,editor,model,index)  当编辑结束时，调用其实现将修改后的数据更新至数据库。其实，它是通过调用Model中的setData()实现数据的更新。

from PySide6 import QtCore
from PySide6.QtCore import QAbstractItemModel, QEvent, QModelIndex, Qt
from PySide6.QtWidgets import QStyleOptionViewItem, QStyledItemDelegate, QTextEdit, QWidget


class TextEditDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex):
        self.parent.resizeRowToContents(index.row())
        editor = QTextEdit(parent)
        editor.setFixedHeight(self.parent.rowHeight(index.row()))
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex):
        value = index.model().data(index, Qt.ItemDataRole.EditRole)
        newTextEdit = editor
        newTextEdit.setPlainText(value)

    def setModelData(self, editor: QWidget,  model: QAbstractItemModel, index: QModelIndex):
        newTextEdit = editor
        value = newTextEdit.toPlainText()
        model.setData(index, value, Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex):
        editor.setGeometry(option.rect)
