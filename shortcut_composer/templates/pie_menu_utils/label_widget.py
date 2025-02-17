# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Protocol

from PyQt5.QtCore import Qt, QMimeData, QEvent
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QDrag, QPixmap, QMouseEvent

from api_krita.pyqt import PixmapTransform, BaseWidget
from .pie_style import PieStyle
from .label import Label


class WidgetInstructions(Protocol):
    """Additional logic to do on entering and leaving a widget."""

    def on_enter(self, label: Label) -> None:
        """Logic to perform when mouse starts hovering over widget."""

    def on_leave(self, label: Label) -> None:
        """Logic to perform when mouse stops hovering over widget."""


class LabelWidget(BaseWidget):
    """Displays a `label` inside of `widget` using given `style`."""

    def __init__(
        self,
        label: Label,
        style: PieStyle,
        parent: QWidget,
        is_unscaled: bool = False,
    ) -> None:
        super().__init__(parent)
        self.setGeometry(0, 0, style.icon_radius*2, style.icon_radius*2)
        self.label = label
        self._style = style
        self._is_unscaled = is_unscaled

        self.draggable = self._draggable = True

        self._enabled = True
        self._hovered = False

        self._instructions: list[WidgetInstructions] = []

    def add_instruction(self, instruction: WidgetInstructions):
        """Add additional logic to do on entering and leaving widget."""
        self._instructions.append(instruction)

    @property
    def draggable(self) -> bool:
        """Return whether the label can be dragged."""
        return self._draggable

    @draggable.setter
    def draggable(self, value: bool) -> None:
        """Make the widget accept dragging or not."""
        self._draggable = value
        if value:
            return self.setCursor(Qt.ArrowCursor)
        self.setCursor(Qt.CrossCursor)

    @property
    def enabled(self):
        """Return whether the label interacts with mouse hover and drag."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Make the widget interact with mouse or not."""
        self._enabled = value
        if not value:
            self.draggable = False
        self.repaint()

    def move_to_label(self) -> None:
        """Move the widget according to current center of label it holds."""
        self.move_center(self.label.center)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        """Initiate a drag loop for this Widget, so Widgets can be swapped."""
        if e.buttons() != Qt.LeftButton or not self._draggable:
            return

        drag = QDrag(self)
        drag.setMimeData(QMimeData())

        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(PixmapTransform.make_pixmap_round(pixmap))

        drag.exec_(Qt.MoveAction)

    def enterEvent(self, e: QEvent) -> None:
        super().enterEvent(e)
        """Notice that mouse moved over the widget."""
        self._hovered = True
        for instruction in self._instructions:
            instruction.on_enter(self.label)
        self.repaint()

    def leaveEvent(self, e: QEvent) -> None:
        """Notice that mouse moved out of the widget."""
        super().leaveEvent(e)
        self._hovered = False
        for instruction in self._instructions:
            instruction.on_leave(self.label)
        self.repaint()

    @property
    def _border_color(self):
        """Return border color which differs when enabled or hovered."""
        if not self.enabled:
            return self._style.active_color_dark
        if self._hovered and self.draggable:
            return self._style.active_color
        return self._style.border_color

    @property
    def icon_radius(self):
        """Return icon radius based flag passed on initialization."""
        if self._is_unscaled:
            return self._style.unscaled_icon_radius
        return self._style.icon_radius
