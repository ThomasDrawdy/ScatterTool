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
        self.normal_lay = self._create_normal_ui_()
        self.layer_lay = self._create_layer_ui_()

        self.main_lay.addLayout(self.input_lay)
        self.main_lay.addLayout(self.layer_lay)
        self.main_lay.addLayout(self.normal_lay)
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
        self.sizex_header_lbl = QtWidgets.QLabel("Random Scale %: ")
        self.sizex_header_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.sizex_le = QtWidgets.QLineEdit("0")
        self.sizex_le.setFixedWidth(40)
        self.sizex_percent_lbl = QtWidgets.QLabel("X")

        self.sizey_header_lbl = QtWidgets.QLabel("")
        self.sizey_header_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.sizey_le = QtWidgets.QLineEdit("0")
        self.sizey_le.setFixedWidth(40)
        self.sizey_percent_lbl = QtWidgets.QLabel("Y")

        self.sizez_header_lbl = QtWidgets.QLabel("")
        self.sizez_header_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.sizez_le = QtWidgets.QLineEdit("0")
        self.sizez_le.setFixedWidth(40)
        self.sizez_percent_lbl = QtWidgets.QLabel("Z")

        self.rotatex_header_lbl = QtWidgets.QLabel("Random Rotation: ")
        self.rotatex_header_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.rotatex_le = QtWidgets.QLineEdit("0")
        self.rotatex_le.setFixedWidth(40)
        self.rotatex_percent_lbl = QtWidgets.QLabel("X")

        self.rotatey_header_lbl = QtWidgets.QLabel("")
        self.rotatey_header_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.rotatey_le = QtWidgets.QLineEdit("0")
        self.rotatey_le.setFixedWidth(40)
        self.rotatey_percent_lbl = QtWidgets.QLabel("Y")

        self.rotatez_header_lbl = QtWidgets.QLabel("")
        self.rotatez_header_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.rotatez_le = QtWidgets.QLineEdit("0")
        self.rotatez_le.setFixedWidth(40)
        self.rotatez_percent_lbl = QtWidgets.QLabel("Z")

        self.perSel_header_lbl = QtWidgets.QLabel("Percentage of Selection: ")
        self.perSel_header_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.perSel_le = QtWidgets.QLineEdit("100")
        self.perSel_le.setFixedWidth(40)
        self.perSel_percent_lbl = QtWidgets.QLabel("%")

        layout = QtWidgets.QGridLayout()
        layout.setColumnStretch(2, 1)
        layout.setColumnMinimumWidth(0, 150)
        layout.addWidget(self.sizex_header_lbl, 0, 0)
        layout.addWidget(self.sizex_le, 0, 1)
        layout.addWidget(self.sizex_percent_lbl, 0, 2)

        layout.addWidget(self.sizey_header_lbl, 1, 0)
        layout.addWidget(self.sizey_le, 1, 1)
        layout.addWidget(self.sizey_percent_lbl, 1, 2)

        layout.addWidget(self.sizez_header_lbl, 2, 0)
        layout.addWidget(self.sizez_le, 2, 1)
        layout.addWidget(self.sizez_percent_lbl, 2, 2)

        layout.addWidget(self.rotatex_header_lbl, 3, 0)
        layout.addWidget(self.rotatex_le, 3, 1)
        layout.addWidget(self.rotatex_percent_lbl, 3, 2)

        layout.addWidget(self.rotatey_header_lbl, 4, 0)
        layout.addWidget(self.rotatey_le, 4, 1)
        layout.addWidget(self.rotatey_percent_lbl, 4, 2)

        layout.addWidget(self.rotatez_header_lbl, 5, 0)
        layout.addWidget(self.rotatez_le, 5, 1)
        layout.addWidget(self.rotatez_percent_lbl, 5, 2)

        layout.addWidget(self.perSel_header_lbl, 6, 0)
        layout.addWidget(self.perSel_le, 6, 1)
        layout.addWidget(self.perSel_percent_lbl, 6, 2)

        return layout

    def _create_normal_ui_(self):

        self.n_align_header_lbl = QtWidgets.QLabel("Normals: ")
        self.n_align_header_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.n_align_cb = QtWidgets.QCheckBox("")
        self.n_align_lbl = QtWidgets.QLabel("Align to Normals")

        layout = QtWidgets.QGridLayout()
        layout.setColumnStretch(2, 1)
        layout.setColumnMinimumWidth(0, 150)

        layout.addWidget(self.n_align_header_lbl, 0, 0)
        layout.addWidget(self.n_align_cb, 0, 1)
        layout.addWidget(self.n_align_lbl, 0, 2)

        return layout

    def _create_layer_ui_(self):
        self.layer_header_lbl = QtWidgets.QLabel("Layers: ")
        self.layer_header_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.layer_le = QtWidgets.QLineEdit("0")
        self.layer_le.setFixedWidth(40)
        self.layer_lbl = QtWidgets.QLabel("")

        self.layer_percent_header_lbl = QtWidgets.QLabel("Percent: ")
        self.layer_percent_header_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.layer_percent_le = QtWidgets.QLineEdit("100")
        self.layer_percent_le.setFixedWidth(40)
        self.layer_percent_lbl = QtWidgets.QLabel("%")

        layout = QtWidgets.QGridLayout()
        layout.setColumnStretch(2, 1)
        layout.setColumnMinimumWidth(0, 150)
        layout.addWidget(self.layer_header_lbl, 0, 0)
        layout.addWidget(self.layer_le, 0, 1)
        layout.addWidget(self.layer_lbl, 0, 2)

        layout.addWidget(self.layer_percent_header_lbl, 1, 0)
        layout.addWidget(self.layer_percent_le, 1, 1)
        layout.addWidget(self.layer_percent_lbl, 1, 2)

        return layout

    def instance(self):

        sel = cmds.ls(sl=1, fl=1)

        objects = cmds.filterExpand(sel, selectionMask=12, expand=1)

        obj_instance = sel[0]

        if len(objects) > 1:
            vertex_names = cmds.ls(sel[1] + '.vtx[*]', fl=1, )
        else:
            vertex_names = cmds.filterExpand(sel, selectionMask=31, expand=1)

        vertex_names = random.sample(vertex_names, int((float(self.perSel_le.text())) * len(vertex_names) * 0.01))

        self._instance_object_(obj_instance, vertex_names, self.rotatex_le.text(),
                               self.rotatey_le.text(), self.rotatez_le.text(), self.n_align_cb.checkState())

    def _instance_object_(self, obj_instance, vertex_names, rotatex, rotatey, rotatez, align):

        if cmds.objectType(obj_instance) == "transform":

            for vertex in vertex_names:
                scalex = (random.random() * (float(self.sizex_le.text())) / 100) + 1
                scaley = (random.random() * (float(self.sizey_le.text())) / 100) + 1
                scalez = (random.random() * (float(self.sizez_le.text())) / 100)+ 1
                turnx = (random.random() * (float(rotatex)))
                turny = (random.random() * (float(rotatey)))
                turnz = (random.random() * (float(rotatez)))

                new_instance = cmds.instance(obj_instance)
                position = cmds.pointPosition(vertex, world=1)
                cmds.move(position[0], position[1], position[2], new_instance, absolute=1, worldSpace=1)
                cmds.scale(scalex, scaley, scalez, new_instance, relative=1, worldSpace=0)

                if align:
                    self._align_vert_(new_instance, vertex, turnx, turny, turnz)

                lay = int(self.layer_le.text())

                if lay > 0:
                    print "225"
                    self._layer_instance_(new_instance, obj_instance, lay)

        else:
            print("Please select a transform to instance.")

    def _align_vert_(self, new_instance, _vert, turnx, turny, turnz):

        cmds.normalConstraint(_vert, new_instance, aimVector=[0.0, 1.0, 0.0], u=[0.0, 0.0, 1.0])

        cmds.normalConstraint(_vert, new_instance, rm=1)

        cmds.rotate(turnx, turny, turnz, new_instance, relative=1, componentSpace=1)

    def _layer_instance_(self, obj, instance, layers):
        if layers <= 0:
            print "242"
            return layers
        else:
            layers = layers - 1
            cmds.select(obj)
            sel = cmds.ls(sl=1, fl=1)

            vertex_names = cmds.ls(sel[0] + '.vtx[*]', fl=1, )
            vertex_names = random.sample(vertex_names, int((float(self.layer_percent_le.text())) * len(vertex_names) * 0.01))

            print vertex_names
            if vertex_names is not None:
                for vertex in vertex_names:
                    scalex = (random.random() * (float(self.sizex_le.text())) / 100) + 1
                    scaley = (random.random() * (float(self.sizey_le.text())) / 100) + 1
                    scalez = (random.random() * (float(self.sizez_le.text())) / 100) + 1
                    turnx = (random.random() * (float(self.rotatex_le.text())))
                    turny = (random.random() * (float(self.rotatex_le.text())))
                    turnz = (random.random() * (float(self.rotatex_le.text())))

                    new_instance = cmds.instance(instance)
                    position = cmds.pointPosition(vertex, world=1)
                    cmds.move(position[0], position[1], position[2], new_instance, absolute=1, worldSpace=1)
                    cmds.scale(scalex, scaley, scalez, new_instance, relative=1, worldSpace=0)

                    if self.n_align_cb.checkState():
                        self._align_vert_(new_instance, vertex, turnx, turny, turnz)

                    self._layer_instance_(new_instance, instance, layers)
                return vertex_names

