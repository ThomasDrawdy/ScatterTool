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

log = logging.getLogger(__name__)



def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterToolUI(QtWidgets.QDialog):

    def __init__(self):
        super(ScatterToolUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter")
        self.setMinimumWidth(500)
        self.setMaximumHeight(200)
        self.create_ui()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.button_lay = self._create_button_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def _create_button_ui(self):
        self.button = QtWidgets.QPushButton('Scatter')
        self.button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.button.clicked.connect(instance)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.button)
        return layout

    def instance(self):

        sel = cmds.ls(sl=1, fl=1)
        print(len(sel))

        objects = cmds.filterExpand(sel, selectionMask=12, expand=1)

        obj_instance = sel[0]

        if len(objects) > 1:
            vertex_names = cmds.ls(sel[1] + '.vtx[*]', fl=1, )
        else:
            vertex_names = cmds.filterExpand(sel, selectionMask=31, expand=1)

        print(len(vertex_names))

        _instance_object_(obj_instance, vertex_names)

    def _instance_object_(obj_instance, vertex_names):

        if cmds.objectType(obj_instance) == "transform":
            print(len(vertex_names))

            for vertex in vertex_names:
                print(cmds.polyNormalPerVertex(vertex, query=1, xyz=1))
                new_instance = cmds.instance(obj_instance)
                position = cmds.pointPosition(vertex, world=1)
                cmds.move(position[0], position[1], position[2], new_instance, absolute=1, worldSpace=1)

        else:
            print("Please select a transform to instance.")

