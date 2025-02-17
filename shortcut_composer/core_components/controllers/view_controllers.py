# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional
from PyQt5.QtGui import QPixmap, QImage
from api_krita import Krita
from api_krita.enums import BlendingMode
from api_krita.pyqt import Text, Colorizer
from ..controller_base import Controller


class ViewBasedController:
    """Family of controllers which operate on values from active view."""

    def refresh(self):
        """Refresh currently stored active view."""
        self.view = Krita.get_active_view()


class PresetController(ViewBasedController, Controller[str]):
    """
    Gives access to `presets`.

    - Operates on `string` representing name of preset
    - Does not have a default

    Example preset name: `"b) Basic-5 Size Opacity"`
    """

    def get_value(self) -> str:
        """Get currently active preset."""
        return self.view.brush_preset

    def set_value(self, value: str) -> None:
        """Set a preset of passed name."""
        self.view.brush_preset = value

    def get_label(self, value: str) -> Optional[QPixmap]:
        """Return the preset icon or None, when there preset name unknown."""
        try:
            image: QImage = Krita.get_presets()[value].image()
        except KeyError:
            return None
        else:
            return QPixmap.fromImage(image)


class BrushSizeController(ViewBasedController, Controller[int]):
    """
    Gives access to `brush size`.

    - Operates on `float` representing brush size in pixels
    - Defaults to `100`
    """

    default_value: float = 100

    def get_value(self) -> float:
        """Get current brush size."""
        return self.view.brush_size

    def set_value(self, value: float) -> None:
        """Set current brush size."""
        self.view.brush_size = value

    def get_label(self, value: float) -> Text:
        """Return Text with formatted brush size."""
        return Text(self.get_pretty_name(value))

    def get_pretty_name(self, value: float) -> str:
        """Format the brush size like: `100px`"""
        return f"{round(value)}px"


class BlendingModeController(ViewBasedController, Controller[BlendingMode]):
    """
    Gives access to `brush blending mode`.

    - Operates on `BlendingMode`
    - Defaults to `BlendingMode.NORMAL`
    """

    default_value = BlendingMode.NORMAL

    def get_value(self) -> BlendingMode:
        """Get currently active blending mode."""
        return self.view.blending_mode

    def set_value(self, value: BlendingMode) -> None:
        """Set a passed blending mode."""
        self.view.blending_mode = value

    def get_label(self, value: BlendingMode) -> Text:
        """Return Label of 3 first letters of mode name in correct color."""
        return Text(value.name[:3], Colorizer.blending_mode(value))

    def get_pretty_name(self, value: BlendingMode) -> str:
        """Forward enums' pretty name."""
        return value.pretty_name


class OpacityController(ViewBasedController, Controller[int]):
    """
    Gives access to `brush opacity` in %.

    - Operates on `integer` in range `0 to 100`
    - Defaults to `100`
    """

    default_value: int = 100

    def get_value(self) -> int:
        """Get current brush opacity."""
        return self.view.opacity

    def set_value(self, value: int) -> None:
        """Set passed brush opacity."""
        self.view.opacity = value

    def get_label(self, value: int) -> Text:
        """Return Text with formatted brush opacity."""
        return Text(self.get_pretty_name(value), Colorizer.percentage(value))

    def get_pretty_name(self, value: float) -> str:
        """Format the opacity like: `100%`"""
        return f"{value}%"


class FlowController(ViewBasedController, Controller[int]):
    """
    Gives access to `brush flow` in %.

    - Operates on `integer` in range `0 to 100`
    - Defaults to `100`
    """

    default_value: int = 100

    def get_value(self) -> int:
        """Get current brush flow."""
        return self.view.flow

    def set_value(self, value: int) -> None:
        """Set passed brush flow."""
        self.view.flow = value

    def get_label(self, value: int) -> Text:
        """Return Text with formatted brush flow."""
        return Text(self.get_pretty_name(value), Colorizer.percentage(value))

    def get_pretty_name(self, value: float) -> str:
        """Format the flow like: `100%`"""
        return f"{value}%"
