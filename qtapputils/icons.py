# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © QtAppUtils Project Contributors
# https://github.com/jnsebgosselin/apputils
#
# This file is part of QtAppUtils.
# Licensed under the terms of the MIT License.
# -----------------------------------------------------------------------------

# ---- Third party imports
from qtpy.QtCore import QSize
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QStyle, QApplication
import qtawesome as qta

# ---- Local imports
from qtapputils.colors import CSS4_COLORS, DEFAULT_ICON_COLOR


DEFAULT_ICON_SIZES = {
    'large': (32, 32),
    'normal': (28, 28),
    'small': (20, 20)
    }


class IconManager:
    """An icon manager for a Qt app."""

    def __init__(self,
                 qta_icons: dict = None,
                 local_icons: dict = None,
                 icon_sizes: dict = DEFAULT_ICON_SIZES,
                 default_color: str = DEFAULT_ICON_COLOR):
        self._qta_icons = qta_icons if qta_icons is not None else {}
        self._local_icons = local_icons if local_icons is not None else {}
        self._default_color = default_color
        self._icon_sizes = icon_sizes

    def get_icon(self, name, color: str = None):
        """Return a QIcon from a specified icon name."""
        if name in self._qta_icons:
            try:
                args, kwargs = self._qta_icons[name]
            except ValueError:
                args = self._qta_icons[name][0]
                kwargs = {}

            if len(args) > 1:
                # For icon made of multiple icons, you need to setup
                # to color in the 'qta_icons' dictionary directly.
                return qta.icon(*args, **kwargs)
            if color is not None:
                # The color passed as argument always supersede the color
                # define in the 'qta_icons' dictionary.
                if color in CSS4_COLORS:
                    kwargs['color'] = CSS4_COLORS[color]
                else:
                    kwargs['color'] = color
            elif color is None and 'color' not in kwargs:
                kwargs['color'] = DEFAULT_ICON_COLOR
            return qta.icon(*args, **kwargs)
        elif name in self._local_icons:
            return QIcon(self._local_icons[name])
        else:
            return QIcon()

    def get_iconsize(self, size: str):
        return QSize(*self._icon_sizes[size])

    @staticmethod
    def get_standard_icon(constant):
        """
        Return a QIcon of a standard pixmap.

        See the link below for a list of valid constants:
        https://srinikom.github.io/pyside-docs/PySide/QtGui/QStyle.html
        """
        constant = getattr(QStyle, constant)
        style = QApplication.instance().style()
        return style.standardIcon(constant)

    def get_standard_iconsize(constant: 'str'):
        """
        Return the standard size of various component of the gui.

        https://srinikom.github.io/pyside-docs/PySide/QtGui/QStyle
        """
        style = QApplication.instance().style()
        if constant == 'messagebox':
            return style.pixelMetric(QStyle.PM_MessageBoxIconSize)
        elif constant == 'small':
            return style.pixelMetric(QStyle.PM_SmallIconSize)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QWidget, QHBoxLayout
    from qtapputils.qthelpers import create_toolbutton, create_qapplication
    from qtapputils.colors import RED

    app = create_qapplication()

    ICOM = IconManager(
        qta_icons={
            'home': [
                ('mdi.home',),
                {'scale_factor': 1.3}],
            'save': [
                ('mdi.content-save',),
                {'color': RED, 'scale_factor': 1.2}],
            }
        )

    window = QWidget()

    icon1 = ICOM.get_icon('home')
    icon2 = ICOM.get_icon('save')

    icon1.pixmap(48).save(
        'D:/Projets/appconfigs/appconfigs/tests/home_icon.png', 'PNG')
    icon2.pixmap(48).save(
        'D:/Projets/appconfigs/appconfigs/tests/save_icon.png', 'PNG')

    layout = QHBoxLayout(window)
    layout.addWidget(create_toolbutton(
        window,
        icon=icon1,
        iconsize=ICOM.get_iconsize('large')
        ))
    layout.addWidget(create_toolbutton(
        window,
        icon=icon2,
        iconsize=ICOM.get_iconsize('small')))

    window.show()

    # pixmap.save(buffer, "PNG")

    sys.exit(app.exec_())
