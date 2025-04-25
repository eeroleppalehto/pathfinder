from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from UserInterface.Components.UIComponents  import UIComponent

class ActiveComponentRegistry:
    """
    Registry for managing the currently active UI component.

    This is primarily used to track the component that is currently active,
    and can be extended to include hovered or focused components as well.
    
    For example, it is used in components like dropdown menus to deactivate
    the previously active component when a new one is activated, ensuring
    that only one remains active at a time.
    """
    def __init__(self):
        self.active:  UIComponent | None = None
        
    def get_active(self):
        return self.active
    
    def set_active(self, component: UIComponent):
        self.active = component

    def clear_active(self):
        self.active = None

class UIRoot:
    """
    UIRoot is the top-level container for all UI components.

    It maintains a list of registered UIComponent instances and a shared
    ActiveComponentRegistry for managing focus, hover states, and behaviors
    such as collapsing dropdown menus. UIRoot handles drawing and event
    propagation across its child components, ensuring consistent UI flow.
    """
    
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
