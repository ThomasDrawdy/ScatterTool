import logging

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc
from pymel.core.system import Path
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import __version__
from shiboken2 import wrapInstance
import random

log = logging.getLogger(__name__)



def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterToolUI(QtWidgets.QDialog):
    rScale = 0
    rRotation = 0

    def __init__(self):
        super(ScatterToolUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter")
        self.setMinimumWidth(400)
        self.setMinimumHeight(150)
        self.create_ui()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter")
        self.title_lbl.setStyleSheet("font: bold 20px")

        self.main_lay = QtWidgets.QVBoxLayout()
        self.button_lay = self._create_button_ui()
        self.input_lay = self._create_input_ui_()

        self.main_lay.addLayout(self.input_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def _create_button_ui(self):
        self.scatter_button = QtWidgets.QPushButton('Scatter')
        self.scatter_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.scatter_button.clicked.connect(self.instance)

        self.close_button = QtWidgets.QPushButton('Close')
        self.close_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_button)
        layout.addWidget(self.close_button)
        return layout

    def _create_input_ui_(self):
        self.size_header_lbl = QtWidgets.QLabel("Random Scale: ")
        self.size_header_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.size_le = QtWidgets.QLineEdit("0")
        self.size_le.setFixedWidth(40)

        self.size_percent_lbl = QtWidgets.QLabel("%")

        self.rotate_header_lbl = QtWidgets.QLabel("Random Rotation: ")
        self.rotate_header_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.rotate_le = QtWidgets.QLineEdit("0")
        self.rotate_le.setFixedWidth(40)

        self.rotate_percent_lbl = QtWidgets.QLabel("")

        layout = QtWidgets.QGridLayout()
        layout.setColumnStretch(2, 1)
        layout.setColumnMinimumWidth(0, 100)
        layout.addWidget(self.size_header_lbl, 0, 0)
        layout.addWidget(self.size_le, 0, 1)
        layout.addWidget(self.size_percent_lbl, 0, 2)

        layout.addWidget(self.rotate_header_lbl, 1, 0)
        layout.addWidget(self.rotate_le, 1, 1)
        layout.addWidget(self.rotate_percent_lbl, 1, 2)

        return layout

    def instance(self):
        self.rScale = self.size_le.text()
        self.rRotation = self.rotate_le.text()

        sel = cmds.ls(sl=1, fl=1)
        #print(len(sel))

        objects = cmds.filterExpand(sel, selectionMask=12, expand=1)

        obj_instance = sel[0]

        if len(objects) > 1:
            vertex_names = cmds.ls(sel[1] + '.vtx[*]', fl=1, )
        else:
            vertex_names = cmds.filterExpand(sel, selectionMask=31, expand=1)

        #print(len(vertex_names))

        _instance_object_(obj_instance, vertex_names)

    def _instance_object_(obj_instance, vertex_names):
        s = self.rScale
        if cmds.objectType(obj_instance) == "transform":
            #print(len(vertex_names))

            for vertex in vertex_names:
                scale = random.random(0, s) 
                #print(cmds.polyNormalPerVertex(vertex, query=1, xyz=1))
                new_instance = cmds.instance(obj_instance)
                position = cmds.pointPosition(vertex, world=1)
                cmds.move(position[0], position[1], position[2], new_instance, absolute=1, worldSpace=1)
                cmds.scale(scale, scale, scale, new_instance, relative=1, worldSpace=1)

        else:
            print("Please select a transform to instance.")

    def get_values(self):
        print self.rScale
        print self.rRotation
