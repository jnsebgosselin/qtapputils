# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © QtAppUtils Project Contributors
# https://github.com/jnsebgosselin/apputils
#
# This file is part of QtAppUtils.
# Licensed under the terms of the MIT License.
# -----------------------------------------------------------------------------

"""Qt utilities"""

from __future__ import annotations
from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from qtpy.QtGui import QIcon

# ---- Standard imports
import sys
import platform
from math import pi

# ---- Third party imports
from qtpy.QtGui import QKeySequence
from qtpy.QtCore import QByteArray, Qt, QSize
from qtpy.QtWidgets import (
    QWidget, QSizePolicy, QToolButton, QApplication, QStyleFactory, QAction,
    QToolBar)

# --- Local imports
from qtapputils.widgets import WaitingSpinner


def qbytearray_to_hexstate(qba):
    """Convert QByteArray object to a str hexstate."""
    return str(bytes(qba.toHex().data()).decode())


def hexstate_to_qbytearray(hexstate):
    """Convert a str hexstate to a QByteArray object."""
    return QByteArray().fromHex(str(hexstate).encode('utf-8'))


def create_mainwindow_toolbar(
        title: str, iconsize: int = None, areas: int = Qt.TopToolBarArea,
        movable: bool = False, floatable: bool = False,
        orientation: int = Qt.Horizontal):
    """Create and return a toolbar with title and object_name."""
    toolbar = QToolBar(title)
    toolbar.setOrientation(orientation)
    toolbar.setObjectName(title.lower().replace(' ', '_'))
    toolbar.setFloatable(floatable)
    toolbar.setMovable(movable)
    toolbar.setAllowedAreas(areas)

    if iconsize is not None:
        toolbar.setIconSize(QSize(iconsize, iconsize))

    return toolbar


def create_qapplication(ft_ptsize: int = None, ft_family: str = None):
    """Create a QApplication instance if it doesn't already exist"""
    qapp = QApplication.instance()
    if qapp is None:
        qapp = QApplication(sys.argv)

        if platform.system() == 'Windows':
            qapp.setStyle(QStyleFactory.create('WindowsVista'))

    ft = qapp.font()
    if ft_ptsize is not None:
        ft.setPointSize(ft_ptsize)
    if ft_family is not None:
        ft.setFamily(ft_family)
    qapp.setFont(ft)

    return qapp


def create_toolbar_stretcher():
    """Create a stretcher to be used in a toolbar """
    stretcher = QWidget()
    stretcher.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return stretcher


def create_toolbutton(parent, text: str = None, shortcut: str = None,
                      icon: QIcon = None, tip: str = None,
                      toggled: Callable = None, triggered: Callable = None,
                      autoraise=True, text_beside_icon: bool = False,
                      iconsize: int | QSize = None):
    """Create a QToolButton with the provided settings."""
    button = QToolButton(parent)
    if text is not None:
        button.setText(text)
    if icon is not None:
        button.setIcon(icon)
    if any((text, tip, shortcut)):
        button.setToolTip(format_tooltip(text, tip, shortcut))
    if text_beside_icon:
        button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
    button.setAutoRaise(autoraise)
    if triggered is not None:
        button.clicked.connect(triggered)
    if toggled is not None:
        button.toggled.connect(toggled)
        button.setCheckable(True)
    if shortcut is not None:
        if isinstance(shortcut, (list, tuple)):
            for sc in shortcut:
                button.setShortcut(sc)
        else:
            button.setShortcut(shortcut)
    if iconsize is not None:
        if isinstance(iconsize, int):
            iconsize = QSize(iconsize, iconsize)
        button.setIconSize(iconsize)
    return button


def create_action(parent, text: str = None, shortcut: str = None,
                  icon: QIcon = None, tip: str = None,
                  toggled: Callable = None, triggered: Callable = None,
                  data=None, menurole=None,
                  context=Qt.WindowShortcut, name: str = None):
    """Create and return a QAction with the provided settings."""
    action = QAction(text, parent)
    action.setShortcutContext(context)
    if triggered is not None:
        action.triggered.connect(triggered)
    if toggled is not None:
        action.toggled.connect(toggled)
        action.setCheckable(True)
    if icon is not None:
        action.setIcon(icon)
    if any((text, tip, shortcut)):
        action.setToolTip(format_tooltip(text, tip, shortcut))
    if text:
        action.setStatusTip(format_statustip(text, shortcut))
    if data is not None:
        action.setData(data)
    if menurole is not None:
        action.setMenuRole(menurole)
    if shortcut is not None:
        if isinstance(shortcut, (list, tuple)):
            action.setShortcuts(shortcut)
        else:
            action.setShortcut(shortcut)
    if name is not None:
        action.setObjectName(name)

    return action


def create_waitspinner(
        size: int = 32, n: int = 11, parent: QWidget = None
        ) -> WaitingSpinner:
    """
    Create a wait spinner.

    Parameters
    ----------
    size : int, optional
        The size of the spinner in integer point precision (one point is equal
        to 1/72 of an inch). The default is 32.
    n : int, optional
        The number of dots used to draw the spinner. The default is 11.
    parent : QWidget, optional
        The parent widget of the spinner. The default is None.

    Returns
    -------
    spinner : WaitingSpinner
        The waitspinner created with the specified parameters
    """
    dot_padding = 1

    # To calculate the size of the dots, we need to solve the following
    # system of two equations in two variables.
    # (1) middle_circumference = pi * (size - dot_size)
    # (2) middle_circumference = n * (dot_size + dot_padding)
    dot_size = (pi * size - n * dot_padding) / (n + pi)
    inner_radius = (size - 2 * dot_size) / 2

    spinner = WaitingSpinner(parent, centerOnParent=False)
    spinner.setTrailSizeDecreasing(True)
    spinner.setNumberOfLines(n)
    spinner.setLineLength(dot_size)
    spinner.setLineWidth(dot_size)
    spinner.setInnerRadius(inner_radius)
    spinner.setColor(Qt.black)

    return spinner


def format_statustip(text: str, shortcuts: list[str] | str):
    """
    Format text and shortcut into a single str to be set
    as an action status tip. The status tip is displayed on all status
    bars provided by the action's top-level parent widget.
    """
    keystr = get_shortcuts_native_text(shortcuts)
    if text and keystr:
        stip = "{} ({})".format(text, keystr)
    elif text:
        stip = "{}".format(text)
    else:
        stip = ""
    return stip


def format_tooltip(text: str, tip: str, shortcuts: list[str] | str):
    """
    Format text, tip and shortcut into a single str to be set
    as a widget's tooltip.
    """
    keystr = get_shortcuts_native_text(shortcuts)
    # We need to replace the unicode characters < and > by their HTML
    # code to avoid problem with the HTML formatting of the tooltip.
    keystr = keystr.replace('<', '&#60;').replace('>', '&#62;')
    ttip = ""
    if text or keystr:
        ttip += "<p style='white-space:pre'><b>"
        if text:
            ttip += "{}".format(text) + (" " if keystr else "")
        if keystr:
            ttip += "({})".format(keystr)
        ttip += "</b></p>"
    if tip:
        ttip += "<p>{}</p>".format(tip or '')
    return ttip


def get_shortcuts_native_text(shortcuts: list[str] | str):
    """
    Return the native text of a shortcut or a list of shortcuts.
    """
    if not isinstance(shortcuts, (list, tuple)):
        shortcuts = [shortcuts, ]

    return ', '.join([QKeySequence(sc).toString(QKeySequence.NativeText)
                      for sc in shortcuts])


def get_default_contents_margins() -> list[int, int, int, int]:
    """
    Return the default [left, top, right, bottom] contents margins
    of a QLayout.
    """
    style = QApplication.instance().style()
    return [
        style.pixelMetric(style.PM_LayoutLeftMargin),
        style.pixelMetric(style.PM_LayoutTopMargin),
        style.pixelMetric(style.PM_LayoutRightMargin),
        style.pixelMetric(style.PM_LayoutBottomMargin),
        ]
