# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Optional

from PyQt5.QtCore import QTimer

from api_krita import Krita
from input_adapter import ComplexAction
from core_components import Instruction
from .slider_handler import SliderHandler


class SingleAxisTracker(ComplexAction):
    """
    Track the mouse along one axis to switch values.

    Tracking is performed as long as the key is pressed.
    This class only grants the ComplexAction interface, while the main
    logic is located in passed SliderHandler.
    """

    def __init__(
        self, *,
        name: str,
        slider_handler: SliderHandler,
        instructions: List[Instruction] = [],
        short_vs_long_press_time: Optional[float] = None
    ) -> None:
        super().__init__(
            name=name,
            short_vs_long_press_time=short_vs_long_press_time,
            instructions=instructions)

        self._handler = slider_handler

    def on_key_press(self) -> None:
        """Start tracking with handler."""
        super().on_key_press()
        self._handler.start()

    def on_every_key_release(self) -> None:
        """End tracking with handler."""
        super().on_every_key_release()
        self._handler.stop()


class DoubleAxisTracker(ComplexAction):
    """
    Track the mouse along the axis which had the biggest initial movement.

    Tracking is performed as long as the key is pressed.
    This class only grants the ComplexAction interface, while the main
    logic is located in SliderHandler which uses passed Slider.
    """

    def __init__(
        self, *,
        name: str,
        horizontal_handler: SliderHandler,
        vertical_handler: SliderHandler,
        instructions: List[Instruction] = [],
        short_vs_long_press_time: Optional[float] = None
    ) -> None:
        super().__init__(
            name=name,
            short_vs_long_press_time=short_vs_long_press_time,
            instructions=instructions)

        self._horizontal_handler = horizontal_handler
        self._vertical_handler = vertical_handler
        self._timer = QTimer()
        self._timer.timeout.connect(self._start_after_picking_slider)

    def on_key_press(self) -> None:
        """Start a timer which decides which handler to start."""
        super().on_key_press()
        self._comparator = self.MouseComparator()
        self._timer.start(50)

    def _start_after_picking_slider(self) -> None:
        """Wait for inital movement to activate the right handler."""
        if self._comparator.delta_x <= 10 and self._comparator.delta_y <= 10:
            return

        if self._comparator.is_horizontal:
            self._horizontal_handler.start()
        else:
            self._vertical_handler.start()
        self._timer.stop()

    def on_every_key_release(self) -> None:
        """End tracking with handler, regardless of which one was started."""
        super().on_every_key_release()
        self._horizontal_handler.stop()
        self._vertical_handler.stop()

    class MouseComparator:
        """Compares current mouse position with position from init phase."""

        def __init__(self) -> None:
            """Store cursor position provider and store starting position."""
            self.cursor = Krita.get_cursor()
            self.start_x = self.cursor.x()
            self.start_y = self.cursor.y()

        @property
        def delta_x(self) -> int:
            """Offset of current position from starting one in x axis."""
            return abs(self.start_x - self.cursor.x())

        @property
        def delta_y(self) -> int:
            """Offset of current position from starting one in y axis."""
            return abs(self.start_y - self.cursor.y())

        @property
        def is_horizontal(self) -> bool:
            """Is offset in x axis bigger than in y axis."""
            return self.delta_x > self.delta_y
