import os,sys
from csv_file import *
from PyQt5 import QtWidgets, uic,QtGui,QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QFontDialog,QFileDialog,QMessageBox,QTableWidgetItem,QMenu,QShortcut,QApplication 

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)
        self.setAcceptDrops(True)
        self.tableWidget.setDragEnabled(True)
        self.New_Table()
        self.Connect_actions()
        self.show()

    def New_Table(self):
        self.CSV_File = CSV()
        self.file_path = ""
        self.filename = ""
        self.data = list()
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.clear()

    def contextMenuEvent(self,event):
        menu = QMenu()
        copy_cell = menu.addAction("Скопировать")
        menu.addSeparator()
        new_column = menu.addAction("Добавить столбец")
        new_row = menu.addAction("Добавить строку")
        menu.addSeparator()
        del_column = menu.addAction("Удалить столбец")
        del_row = menu.addAction("Удалить строку")
        menu.addSeparator()
        clear_cell = menu.addAction("Очистить ячейку")
        try:
            action = menu.exec_(self.mapToGlobal(event.pos()))
            if action == new_row:
                self.Insert_Row()
            elif action == copy_cell:
                self.Copy_To_FrameBuffer()
            elif action == new_column:
                self.Insert_Column()
            elif action == del_row:
                self.tableWidget.removeRow(self.tableWidget.currentRow())
            elif action == del_column:
                self.tableWidget.removeColumn(self.tableWidget.currentColumn())
            elif action == clear_cell:
                self.tableWidget.setItem(self.tableWidget.currentRow(),self.tableWidget.currentColumn(),QTableWidgetItem(""))
        except Exception as ex:
            print(ex)
        #menu.addSeperator()

    def Connect_actions(self):
        self.action.triggered.connect(self.New_Table)
        self.action_2.triggered.connect(self.Open_File)
        self.action_10.triggered.connect(self.Insert_Column)
        self.action_11.triggered.connect(self.Insert_Row)
        self.action_13.triggered.connect(self.Remove_Column)
        self.action_14.triggered.connect(self.Remove_Row)
        self.action_6.triggered.connect(self.close)
        self.action_8.triggered.connect(self.Show_Fonts)
        self.action_3.triggered.connect(self.Save_File)
        self.action_4.triggered.connect(self.Save_File_As)
        self.tableWidget.cellChanged.connect(self.Update_Cell)
        QShortcut(QKeySequence("Ctrl+C"), self).activated.connect(self.Copy_To_FrameBuffer)

    def dragEnterEvent(self,event):
        try:
            print(event.mimeData().text())
        except Exception as ex:
            print("1")

    def Copy_To_FrameBuffer(self):
        if len(self.tableWidget.selectedItems()) > 0:
            try:
                temp_clipboard = str()
                for item in self.tableWidget.selectedItems():
                    if item is None:
                        pass
                    else:
                        temp_clipboard += item.text()+";"
                temp_clipboard=temp_clipboard[:-1]
                QApplication.clipboard().setText(temp_clipboard)
            except Exception as ex:
                print(ex)
        else:
            print("Нечего копировать")

    def Update_Cell(self,row,column):
        try:
            self.CSV_File.Update(column,row,self.tableWidget.item(row,column).text())
            self.CSV_File.Save(filename="temp.csv",delem=";")
        except IndexError:
            print("Нужно обновить файл.")
            self.Update_dat()
            self.CSV_File.Update(column,row,self.tableWidget.item(row,column).text())
            self.CSV_File.Save(filename="temp.csv",delem=";")

    def Update_dat(self):
        try:
            Y_SIZE = self.tableWidget.rowCount()
            X_SIZE = self.tableWidget.columnCount()
            self.CSV_File.data = [["" for x in range(X_SIZE)] for y in range(Y_SIZE)] 
            for y in range(self.tableWidget.rowCount()):
                for x in range(self.tableWidget.columnCount()):
                    if self.tableWidget.item(y,x) is None:
                        self.CSV_File.Update(y,x,"")
                    else:
                        self.CSV_File.Update(y,x,self.tableWidget.item(y,x).text())
        except Exception as ex:
            print(ex)

    def Save_File_As(self):
        data = QFileDialog.getSaveFileName(caption="Выберите файл",
                                           filter="Разделитель ; точка с запятой(*.csv);;Разделитель : двоеточие(*.csv);;Разделитель , запятая(*.csv)")
        if data[0] and data[1]:
            if ',' in data[1]:
                dele = ","
            elif ';' in data[1]:
                dele = ";"
            elif ':' in data[1]:
                dele = ":"
            else:
                dele = ";"
            self.CSV_File.Save(filename=data[0],delem=dele)
            self.file_path = data[0]
            self.filename = self.file_path[self.file_path.rfind("/")+1:]
        else:
            print("Файл не выбран")
    
    def Save_File(self):
        print(self.filename,self.file_path)
        if self.filename == "":
            self.Save_File_As()
        else:
            try:
                self.CSV_File.Save(filename=self.file_path)
            except Exception as ex:
                print(ex)

    def Show_Fonts(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.tableWidget.setFont(font)

    def Remove_Column(self):
        if self.tableWidget.columnCount()>0:
            self.tableWidget.setColumnCount(self.tableWidget.columnCount()-1)

    def Remove_Row(self):
        if self.tableWidget.rowCount()>0:
            self.tableWidget.setRowCount(self.tableWidget.rowCount()-1)

    def Insert_Column(self):
        self.tableWidget.setColumnCount(self.tableWidget.columnCount()+1)

    def Insert_Row(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)

    def Open_File(self):
        self.tableWidget.cellChanged.disconnect(self.Update_Cell)
        data = QFileDialog.getOpenFileName(caption="Выберите файл",
                                           filter="Разделитель ; точка с запятой(*.csv);;Разделитель : двоеточие(*.csv);;Разделитель , запятая(*.csv)")
        if data[0] and data[1]:
            if ',' in data[1]:
                dele = ","
            elif ';' in data[1]:
                dele = ";"
            elif ':' in data[1]:
                dele = ":"
            else:
                dele = ";"
            try:
                self.CSV_File.Load(filename=data[0],delem=dele)
                self.file_path = data[0]
                self.filename = self.file_path[self.file_path.rfind("/")+1:]
                self.tableWidget.setRowCount(self.CSV_File.rows())
                self.tableWidget.setColumnCount(self.CSV_File.columns())
                for y in range(self.CSV_File.rows()):
                    for x in range(self.CSV_File.columns()):
                        self.tableWidget.setItem(y,x,QTableWidgetItem(self.CSV_File.data[y][x]))
                self.tableWidget.cellChanged.connect(self.Update_Cell)
            except Exception as ex:
                print(ex)
        else:
            print("Не выбран файл")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
