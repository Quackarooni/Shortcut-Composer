# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita import Krita
from api_krita.enums import BlendingMode, NodeType
from api_krita.pyqt import Text, Colorizer
from ..controller_base import Controller


class NodeBasedController:
    """Family of controllers which operate on values from active node."""

    def refresh(self):
        """Refresh currently stored active node."""
        self.active_document = Krita.get_active_document()
        self.active_node = self.active_document.active_node


class LayerOpacityController(NodeBasedController, Controller[int]):
    """
    Gives access to active layers' `opacity` in %.

    - Operates on `integer` in range `0 to 100`
    - Defaults to `100`
    """

    default_value: int = 100

    def get_value(self) -> int:
        """Get currently active blending mode."""
        return self.active_node.opacity

    def set_value(self, opacity: int) -> None:
        """Set a passed blending mode."""
        if self.active_node.opacity != opacity:
            self.active_node.opacity = opacity
            self.active_document.refresh()

    def get_label(self, value: int) -> Text:
        """Return Text with formatted layer opacity."""
        return Text(self.get_pretty_name(value), Colorizer.percentage(value))

    def get_pretty_name(self, value: float) -> str:
        """Format the layer opacity like: `100%`"""
        return f"{value}%"


class LayerBlendingModeController(NodeBasedController,
                                  Controller[BlendingMode]):
    """
    Gives access to active layers' `blending mode`.

    - Operates on `BlendingMode`
    - Defaults to `BlendingMode.NORMAL`
    """

    default_value = BlendingMode.NORMAL

    def get_value(self) -> BlendingMode:
        """Get current brush opacity."""
        return self.active_node.blending_mode

    def set_value(self, blending_mode: BlendingMode) -> None:
        """Set passed brush opacity."""
        if self.active_node.blending_mode != blending_mode:
            self.active_node.blending_mode = blending_mode
            self.active_document.refresh()

    def get_label(self, value: BlendingMode) -> Text:
        """Return Label of 3 first letters of mode name in correct color."""
        return Text(value.name[:3], Colorizer.blending_mode(value))

    def get_pretty_name(self, value: BlendingMode) -> str:
        """Forward enums' pretty name."""
        return value.pretty_name


class LayerVisibilityController(NodeBasedController, Controller[bool]):
    """
    Gives access to active layers' `visibility`.

    - Operates on `bool`
    - Defaults to `True`
    """

    default_value: bool = True

    def get_value(self) -> bool:
        """Get current brush opacity."""
        return self.active_node.visible

    def set_value(self, visibility: bool) -> None:
        """Set passed brush opacity."""
        if self.active_node.visible != visibility:
            self.active_node.visible = visibility
            self.active_document.refresh()


class CreateLayerWithBlendingController(NodeBasedController,
                                        Controller[BlendingMode]):
    """Creates Paint Layer with set Blending Mode."""

    default_value = BlendingMode.NORMAL

    def get_value(self) -> BlendingMode:
        """Get current layer blending mode."""
        raise NotImplementedError("Can't use this controller to get value")

    def set_value(self, blending_mode: BlendingMode) -> None:
        """Create new paint layer and set blending mode."""
        layer = self.active_document.create_node(
            name=str(blending_mode.value).capitalize() + " Paint Layer",
            node_type=NodeType.PAINT_LAYER)
        layer.blending_mode = blending_mode
        parent = self.active_node.get_parent_node()
        parent.add_child_node(layer, self.active_node)

    def get_label(self, value: BlendingMode) -> Text:
        """Return Label of 3 first letters of mode name in correct color."""
        return Text("+" + value.name[:3], Colorizer.blending_mode(value))

    def get_pretty_name(self, value: BlendingMode) -> str:
        """Forward enums' pretty name."""
        return value.pretty_name
