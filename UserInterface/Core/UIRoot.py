from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from UserInterface.Components.UIComponents  import UIComponent

class ActiveComponentRegistry:
    def __init__(self):
        self.active:  UIComponent | None = None
        
    def get_active(self):
        return self.active
    
    def set_active(self, component: UIComponent):
        self.active = component

    def clear_active(self):
        self.active = None

class UIRoot:
    def __init__(self):
        self._components: list[UIComponent] = []
        self.registry = ActiveComponentRegistry()

    def add_component(self, comp: UIComponent) -> None:
        if comp in self._components:
            return
        comp.set_root(self)
        self._components.append(comp)

    def remove_component(self, comp: UIComponent) -> None:
        if comp in self._components:
            self._components.remove(comp)
            comp.set_root(None)

    def draw(self, surface) -> None:
        for comp in self._components:
            comp.draw(surface)
        

    def handle_event(self, event) -> None:
        for comp in self._components:
            comp.handle_event(event)
