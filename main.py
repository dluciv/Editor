#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import json
import os


def try_except(function):
    """
    https://www.blog.pythonlibrary.org/2016/06/09/python-how-to-create-an-exception-logging-decorator/
    """
    import functools

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            print("Exception in " + function.__name__ + ": " + repr(e))
            raise
    return wrapper

# class Main(QtWidgets.QMainWindow):
class Main(QtWidgets.QWidget):

    def __init__(self, parent=None):
        # QtWidgets.QMainWindow.__init__(self, parent)
        super(Main,self).__init__()

        # Rigthr layout for json
        # self.j_tree = QtWidgets.QTextEdit()
        # self.j_tree = QtWidgets.QTreeWidget()
        self.j_tree = QtWidgets.QTreeView()

        self.j_annot = QtWidgets.QTreeView()

        # Left layout for text doc
        self.text_doc = QtWidgets.QPlainTextEdit()

        self.filename = None

        self.initUI()

        self.data = None
        # Open the annotation
        self.j_tree.clicked.connect(self.openElement)

    def initUI(self):
        #Common Form
        hbox = QtWidgets.QVBoxLayout()

        # Rigthr layout for json
        # j_tree = QtWidgets.QTextEdit()
        # j_annot = QtWidgets.QTextEdit()

        # Left layout for text doc
        #  text_doc = QtWidgets.QTextEdit()

        # Create a vert. splitter
        splitter1 = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter1.addWidget(self.j_tree)
        splitter1.addWidget(self.j_annot)
        splitter1.setSizes([200,100])

        # Create a horiz. splitter
        splitter2 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter2.addWidget(self.text_doc)
        splitter2.addWidget(splitter1)

        # Create an open button
        open_btn = QtWidgets.QPushButton("Open", self)
        open_btn.setFixedSize(100,30)
        # Connection
        open_btn.clicked.connect(self.open)

        hbox.addWidget(open_btn)
        hbox.addWidget(splitter2)

        self.setLayout(hbox)

        self.setWindowTitle("Writer")

        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

    def new(self):

        spawn = Main(self)
        spawn.show()


    def load_group_tree(self, data):
        pass

    def load_groups(self, elements):

         for text in elements["Benchmarks"]:
             item = QtGui.QStandardItem(text["name"])
             item.setData(1)

             child = text["group_ids"]
             for test in child:
                test1=QtGui.QStandardItem(str(test)) #читает только text  данные ?
                # item.setChild(i,1,test1)
                item.appendRow(test1)
                test1.setData(2)

             self.model.appendRow(item)

    @try_except
    def openElement(self, checked):
        print(checked)
        # Get the index of chosen element
        index = self.j_tree.currentIndex()
        # Get the name of chosen element(two var-ts)
        # item = QtCore.QModelIndex.data(index)
        # work = self.model.data(index)
        #

        item = self.model.itemFromIndex(index)
        # Get the data that was put in item before
        item_data =  QtGui.QStandardItem.data(item)
        item_text = QtGui.QStandardItem.text(item)
        if item_data == 1:
            # load annotation
            self.j_annot.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.model_annot = QtGui.QStandardItemModel()
            self.load_annot(item_text, self.data)

            self.j_annot.setModel(self.model_annot)
            self.model_annot.setHorizontalHeaderLabels([self.tr("Annotation")])


    def load_annot(self, check, elements):
        for text in elements["Benchmarks"]:
            elem = QtGui.QStandardItem(text["name"])
            elem_text = QtGui.QStandardItem.text(elem)
            if elem_text == check:
                annot = QtGui.QStandardItem(text["annotation"])
                self.model_annot.appendRow(annot)

    # def load_annot(self, parent, elements):
    #
    #      for text in elements["Groups"]:
    #          item = QtGui.QStandardItem(text["Annotation"])
    #
    #          child = text["Duplicates"]
    #          for test in child:
    #             test1=QtGui.QStandardItem(str(test))
    #             item.appendRow(test1)
    #
    #          self.model.appendRow(item)


    @try_except  # если это писать перед функцией, то она перестанет вылетать молча
    def open(self, checked):
        print(checked)  # Этот аргумент есть у события clicked @try_except требует, чтобы все аргументы были описаны
        # Get filename and show only .txt files
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', ".", " (*.txt)")[0]

        if self.filename:
            # Бенчмарки всегда хранятся в файле <имя документа>.json
            bmks_filename = self.filename + '.json'
            with open(self.filename, "r+", encoding='utf-8') as file, open(bmks_filename, "r+", encoding='utf-8') as j_file: # ! dluciv
                self.text_doc.setPlainText(file.read())
                self.data = json.load(j_file)
                # for g in data["Benchmarks"]:
                #      print(g["group_ids"][0])

                # load groups
                self.j_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                self.model = QtGui.QStandardItemModel()
                self.load_groups( self.data)

                self.j_tree.setModel(self.model)
                self.model.setHorizontalHeaderLabels([self.tr("Benchmarks")])

                # load annototion
                # self.j_annot.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                # self.model = QtGui.QStandardItemModel()
                # self.load_annot(self.model, data)

                # self.j_annot.setModel(self.model)
                # self.model.setHorizontalHeaderLabels([self.tr("Annotation")])


            # for g in data["Groups"]:
            #    print(repr(g))
            #     self.j_tree.
            # ... и дальше строим дерево
            # рекомендую https://pythonspot.com/pyqt5-treeview/ ----> QStandardItemModel


def main():
    app = QtWidgets.QApplication(sys.argv)

    main = Main()
    main.show()


    sys.exit(app.exec_())


if __name__ == "__main__":
    main()