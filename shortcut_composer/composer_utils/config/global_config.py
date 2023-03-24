# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar
from enum import Enum

from .fields import FieldBase, ImmutableField

T = TypeVar('T', bound=Enum)


class Config:
    """
    Configuration fields available in the plugin.

    Each field can:
    - return its default value
    - read current value from krita config file in correct type
    - write given value to krita config file

    Class holds a staticmethod which resets all config files.

    VALUES configs are string representations of lists. They hold values
    to use in given action with elements separated with tabulators.
    These are needed to be further parsed using TagConfigValues or
    EnumConfigValues.
    """

    SHORT_VS_LONG_PRESS_TIME = ImmutableField("Short vs long press time", 0.3)
    TRACKER_SENSITIVITY_SCALE = ImmutableField(
        "Tracker sensitivity scale", 1.0)
    TRACKER_DEADZONE = ImmutableField("Tracker deadzone", 0)
    FPS_LIMIT = ImmutableField("FPS limit", 60)
    PIE_GLOBAL_SCALE = ImmutableField("Pie global scale", 1.0)
    PIE_ICON_GLOBAL_SCALE = ImmutableField("Pie icon global scale", 1.0)
    PIE_DEADZONE_GLOBAL_SCALE = ImmutableField(
        "Pie deadzone global scale", 1.0)
    PIE_ANIMATION_TIME = ImmutableField("Pie animation time", 0.2)

    @classmethod
    def reset_defaults(cls) -> None:
        """Reset all config files."""
        for config_field in cls.__dict__.values():
            if isinstance(config_field, FieldBase):
                config_field.reset_default()

    @classmethod
    def get_sleep_time(cls) -> int:
        """Read sleep time from FPS_LIMIT config field."""
        fps_limit = cls.FPS_LIMIT.read()
        return round(1000/fps_limit) if fps_limit else 1
