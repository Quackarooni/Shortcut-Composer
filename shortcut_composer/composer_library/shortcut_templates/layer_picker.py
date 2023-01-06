from enum import Enum
from typing import List

from ..krita_api import Krita, controllers
from ..krita_api.wrappers import Document, Node
from .mouse_tracker import SingleAxisTracker
from .slider_utils import Slider
from .instructions.layer_hide import Instruction


class PickStrategy(Enum):
    @staticmethod
    def __pick_all(document: Document) -> List[Node]:
        return document.all_nodes()

    @staticmethod
    def __pick_visible(document: Document) -> List[Node]:
        nodes = document.all_nodes()
        current_node = document.current_node()
        return [node for node in nodes
                if node.is_visible() or node == current_node]

    ALL = __pick_all
    VISIBLE = __pick_visible


class LayerPicker(SingleAxisTracker):
    def __init__(
        self,
        action_name: str,
        additional_instructions: List[Instruction],
        pick_strategy: PickStrategy = PickStrategy.ALL,
        sensitivity: float = 50.0
    ):
        super().__init__(
            action_name=action_name,
            sign=-1,
            slider=Slider(
                controller=controllers.LayerController(),
                values_to_cycle=[0],
                default_value=None,
                additional_instructions=additional_instructions,
                sensitivity=sensitivity
            ))
        self.hide_strategy = additional_instructions
        self.pick_strategy = pick_strategy

    def on_key_press(self) -> None:
        document = Krita.get_active_document()
        self.slider.set_values_to_cycle(self.pick_strategy(document))
        super().on_key_press()
