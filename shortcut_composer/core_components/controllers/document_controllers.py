# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita import Krita
from api_krita.wrappers import Node
from api_krita.pyqt import Text
from ..controller_base import Controller


class DocumentBasedController:
    """Family of controllers which operate on values from active document."""

    def refresh(self):
        """Refresh currently stored active document."""
        self.document = Krita.get_active_document()


class ActiveLayerController(DocumentBasedController, Controller[Node]):
    """
    Gives access to nodes (layers, groups, masks...) from layer stack.

    - Operates on internal layer objects. Use `CurrentLayerStack(...)`
      to always use current layer stack
    - Does not have a default
    """

    def get_value(self) -> Node:
        """Get current node."""
        return self.document.active_node

    def set_value(self, value: Node) -> None:
        """Set passed node as current."""
        self.document.active_node = value

    def get_pretty_name(self, value: Node) -> str:
        """Forward enums' pretty name."""
        return value.name


class TimeController(DocumentBasedController, Controller[int]):
    """
    Gives access to animation timeline.

    - Operates on `positive integers` representing `frame numbers`
    - Defaults to `0`
    """

    default_value = 0

    def get_value(self) -> int:
        """Get current frame on animation timeline."""
        return self.document.current_time

    def set_value(self, value: int) -> None:
        """Set passed frame of animation timeline as active."""
        self.document.current_time = value

    def get_label(self, value: int) -> Text:
        """Return Text with frame id as string."""
        return Text(self.get_pretty_name(value))
