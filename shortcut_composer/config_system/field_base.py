# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic, Callable, List
from abc import ABC, abstractmethod
from enum import Enum

from .api_krita import Krita
from .parsers import Parser, BoolParser, EnumParser, BasicParser
from .field import Field

T = TypeVar('T')
E = TypeVar('E', bound=Enum)
ListT = TypeVar('ListT', bound=List[Enum])


class FieldBase(ABC, Field, Generic[T]):
    """Implementation base of List, and NonList field."""

    def __new__(cls, *args, **kwargs) -> 'FieldBase[T]':
        obj = object.__new__(cls)
        obj.__init__(*args, **kwargs)
        return obj

    def __init__(
        self,
        config_group: str,
        name: str,
        default: T,
    ):
        self.config_group = config_group
        self.name = name
        self.default = default
        self._on_change_callbacks: List[Callable[[], None]] = []

    def register_callback(self, callback: Callable[[], None]):
        """Store callback in internal list."""
        self._on_change_callbacks.append(callback)

    def write(self, value: T):
        """Write value to file and run callbacks if it was not redundant."""
        if not isinstance(value, type(self.default)):
            raise TypeError(f"{value} not of type {type(self.default)}")

        if self._is_write_redundant(value):
            return

        Krita.write_setting(
            group=self.config_group,
            name=self.name,
            value=self._to_string(value))
        for callback in self._on_change_callbacks:
            callback()

    @abstractmethod
    def read(self) -> T:
        """Return value from kritarc parsed to field type."""
        ...

    @abstractmethod
    def _to_string(self, value: T) -> str:
        """Convert a value of field type to string."""
        ...

    def _is_write_redundant(self, value: T) -> bool:
        """
        Return if writing a value is not necessary.

        That is when:
        - the value is the same as the one stored in file
        - value is a default one and it is not present in file
        """
        if self.read() == value:
            return True
        raw = Krita.read_setting(self.config_group, self.name)
        return raw is None and value == self.default

    def reset_default(self) -> None:
        """Write a default value to kritarc file."""
        self.write(self.default)

    @staticmethod
    def _get_parser(parser_type: type) -> Parser[T]:
        """Return field parser."""
        if issubclass(parser_type, Enum):
            return EnumParser(parser_type)  # type: ignore

        return {
            int: BasicParser(int),
            float: BasicParser(float),
            str: BasicParser(str),
            bool: BoolParser()
        }[parser_type]  # type: ignore
