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
        self.setMinimumHeight(170)
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
        self.close_button.clicked.connect(self.close)

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

        self.rotatex_header_lbl = QtWidgets.QLabel("Random X Rotation: ")
        self.rotatex_header_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.rotatex_le = QtWidgets.QLineEdit("0")
        self.rotatex_le.setFixedWidth(40)

        self.rotatex_percent_lbl = QtWidgets.QLabel("")

        self.rotatey_header_lbl = QtWidgets.QLabel("Random Y Rotation: ")
        self.rotatey_header_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.rotatey_le = QtWidgets.QLineEdit("0")
        self.rotatey_le.setFixedWidth(40)

        self.rotatey_percent_lbl = QtWidgets.QLabel("")

        self.rotatez_header_lbl = QtWidgets.QLabel("Random Z Rotation: ")
        self.rotatez_header_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.rotatez_le = QtWidgets.QLineEdit("0")
        self.rotatez_le.setFixedWidth(40)

        self.rotatez_percent_lbl = QtWidgets.QLabel("")

        layout = QtWidgets.QGridLayout()
        layout.setColumnStretch(2, 1)
        layout.setColumnMinimumWidth(0, 100)
        layout.addWidget(self.size_header_lbl, 0, 0)
        layout.addWidget(self.size_le, 0, 1)
        layout.addWidget(self.size_percent_lbl, 0, 2)

        layout.addWidget(self.rotatex_header_lbl, 1, 0)
        layout.addWidget(self.rotatex_le, 1, 1)
        layout.addWidget(self.rotatex_percent_lbl, 1, 2)

        layout.addWidget(self.rotatey_header_lbl, 2, 0)
        layout.addWidget(self.rotatey_le, 2, 1)
        layout.addWidget(self.rotatey_percent_lbl, 2, 2)

        layout.addWidget(self.rotatez_header_lbl, 3, 0)
        layout.addWidget(self.rotatez_le, 3, 1)
        layout.addWidget(self.rotatez_percent_lbl, 3, 2)

        return layout

    def instance(self):
        self.rScale = self.size_le.text()

        sel = cmds.ls(sl=1, fl=1)

        objects = cmds.filterExpand(sel, selectionMask=12, expand=1)

        obj_instance = sel[0]

        if len(objects) > 1:
            vertex_names = cmds.ls(sel[1] + '.vtx[*]', fl=1, )
        else:
            vertex_names = cmds.filterExpand(sel, selectionMask=31, expand=1)

        self._instance_object_(obj_instance, vertex_names, self.size_le.text(), self.rotatex_le.text(),
                               self.rotatey_le.text(), self.rotatez_le.text())

    def _instance_object_(self, obj_instance, vertex_names, size, rotatex, rotatey, rotatez):

        if cmds.objectType(obj_instance) == "transform":

            for vertex in vertex_names:
                scale = (random.random() * (float(size)/100)) + 1
                turnx = (random.random() * (float(rotatex)))
                turny = (random.random() * (float(rotatey)))
                turnz = (random.random() * (float(rotatez)))
                new_instance = cmds.instance(obj_instance)
                position = cmds.pointPosition(vertex, world=1)
                cmds.move(position[0], position[1], position[2], new_instance, absolute=1, worldSpace=1)
                cmds.scale(scale, scale, scale, new_instance, relative=1, worldSpace=1)
                cmds.rotate(turnx, turny, turnz, new_instance, relative=1, componentSpace=1)

        else:
            print("Please select a transform to instance.")

    def get_values(self):
        print self.rScale
        print self.rRotation
