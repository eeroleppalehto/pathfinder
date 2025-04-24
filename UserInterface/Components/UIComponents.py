from __future__ import annotations
import pygame
import inspect
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP
from UserInterface.Styles.StyleManager import InlineStyle, ComponentStyleManager
from UserInterface.Styles.StyleSheet import StyleGroup, StyleSheet
from UserInterface.Styles.StyleEnums import StyleProperty, StyleType
from UserInterface.Defaults.DefaultStyles import DefaultStyles 
from UserInterface.Core.UIRoot import UIRoot




class UIComponent(InlineStyle):
    """
    The base building block for everything in the UI.
    Manages position, size, style, parent/child hierarchy,
    event propagation, and activation state.
    """
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], component_name: str, style_group: StyleGroup):
        self._local_position = pos  
        self._size = size
        self.active = True
        self.hovered = False
        self.children: list[UIComponent] = []
        self.style_manager = ComponentStyleManager(component_name, style_group.normal, style_group.hover)
        self.parent: UIComponent | None = None
        self.root: UIRoot | None = None
        self._name = "DEFAULT"
    
    @property
    def name(self):
        return self._name

    def set_root(self, root: UIRoot | None):
        self.root = root
        for child in self.children:
            child.set_root(root)
    
    def add_children(self, children: list[UIComponent]):
        for child in children:
            if child.parent is not None:
                child.parent.remove_child(child)
            child.parent = self
            child.set_root(self.root)
            self.children.append(child)
            

    def remove_children(self, children: list[UIComponent]) -> None:
        for child in children:
            if child in self.children:
                self.children.remove(child)
                child.parent = None
                child.set_root(None)

    def set_parent(self, parent: UIComponent) -> None:
        parent.add_child(self)

    def get_absolute_position(self) -> tuple[int, int]:
        if self.parent:
            parent_x, parent_y = self.parent.get_absolute_position()
            local_x, local_y = self._local_position
            return (parent_x + local_x, parent_y + local_y)
        else:
            return self._local_position

    def get_position(self):
        return self.get_absolute_position()

    def set_position(self, x, y):
        self._local_position = (x, y)

    def get_size(self):
        return self._size
    
    def set_size(self, width, height):
        self._size = (width, height)

    def get_rect(self):
        abs_pos = self.get_absolute_position()
        return pygame.Rect(abs_pos[0], abs_pos[1], self._size[0], self._size[1])

    def set_style(self, style: StyleSheet):
        if self.style_manager.normal_style_exists():
            old_style = self.style_manager.get_normal_style()
            old_style.remove_from_object_refereces(self)
        
        style.add_to_object_references(self)
        self.style_manager.set_normal_style(style, self.name)

        for child in self.children:
            child.style_manager.set_normal_style(style, self.name)

    def set_hover_style(self, style: StyleSheet):
        if self.style_manager.hover_style_exists():
            old_style = self.style_manager.get_hover_style()
            old_style.remove_from_object_refereces(self)
        
        style.add_to_object_references(self)
        self.style_manager.set_hover_style(style, self.name)

        for child in self.children:
            child.style_manager.set_hover_style(style, self.name)

    def get_style_property(self, property: StyleProperty, is_hovered: bool, is_computed: bool = False):
        return self.style_manager.get_resolved_property(property, is_hovered, is_computed)
        
    def set_style_property(self, property: StyleProperty, value):
        self.style_manager.set_override(property, value)

    def get_font(self) -> pygame.font.Font | None:
        return self.style_manager.get_resolved_font(self.hovered)

    def get_active_style(self):
        return self.hover_style if self.hovered else self.style

    def draw_children(self, surface):
        for child in self.children:
            child.draw(surface)

    def propagate_event(self, event):
        # Shtitty implentation probably should bubble up from the last element in the tree. 
        for child in self.children:
            child.handle_event(event)

    def handle_event(self, event):
        self.propagate_event(event) 
        return False
    
    def activate(self):
        if(self.root != None):
            active_component = self.root.registry.get_active()
            if(active_component and active_component != self):
                active_component.deactivate()
            self.root.registry.set_active(self)

    def deactivate(self):
        return
    
    
    
class Panel(UIComponent):
    """
    A simple container that draws a colored rectangle (with optional border)
    and can hold other components. Supports click callbacks and hover detection.
    """
    def __init__(self, pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (0, 0), callback: callable = None):
        super().__init__(pos, size, "PANEL", DefaultStyles.Panel)
        self._name = "PANEL"
        self.callback = callback
        
  
    def draw(self, surface):
        rect = self.get_rect()
        background_color = self.get_style_property(StyleProperty.BACKGROUND_COLOR, self.hovered, True)
        border_size = self.get_style_property(StyleProperty.BORDER_SIZE, self.hovered)

        pygame.draw.rect(surface, background_color, rect)
        if border_size > 0:
            border_color = self.get_style_property(StyleProperty.BORDER_COLOR, self.hovered)
            pygame.draw.rect(surface, border_color, rect, border_size)

        self.draw_children(surface)

    def handle_event(self, event):
        rect = self.get_rect()
        if event.type == MOUSEMOTION:
            was_hovered = self.hovered
            self.hovered = rect.collidepoint(event.pos)
            changed = self.hovered != was_hovered
            self.propagate_event(event)
            return changed

        elif event.type == MOUSEBUTTONDOWN and self.hovered:
            if self.callback:
                self.callback()
            self.propagate_event(event)
            self.activate()
            return True

        self.propagate_event(event)
        return False


class Header(UIComponent):
    """
    A text label component that auto-sizes itself to fit its multi-line text.
    Caches its rendered surface for efficiency and supports background,
    text color, and alignment styles.
    """
    def __init__(self, pos: tuple[int, int], text: str):
        super().__init__(pos, (0, 0), "HEADER", DefaultStyles.Header)
        self._name = "HEADER"
        self._text = text
        self._font = self.style_manager.get_resolved_font(StyleType.NORMAL)
        
        self._cache_key = None
        self._cached_surf = None
        self.needs_update = True
        self.update_size()

    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, string: str):
        if self._text != string:
            self._text = string
            self.update_size()
            self.needs_update = True
    
    def set_text_content(self, text: str):
        if self._text != text:
            self._text = text
            self.update_size()
            self.needs_update = True

    def set_position(self, x: int, y: int):
        super().set_position(x, y)
        self.needs_update = True

    def update_size(self):
        lines = self._text.split('\n') if self._text else ['']
        line_height = self._font.get_linesize()
        max_width = max(self._font.size(line)[0] for line in lines)
        total_height = line_height * len(lines)
        self.set_size(max_width, total_height)
        self.needs_update = True

    def draw(self, surface):
        rect = self.get_rect()
        bg_color = self.get_style_property(StyleProperty.BACKGROUND_COLOR, self.hovered, True)
        text_color = self.get_style_property(StyleProperty.TEXT_COLOR, self.hovered, True)
        alignment = self.get_style_property(StyleProperty.TEXT_ALIGN, self.hovered) or 'left'
        
        if bg_color is not None:
            pygame.draw.rect(surface, bg_color, rect)

        
        cache_key = (self._text, text_color, alignment)
        if self.needs_update or self._cache_key != cache_key or self._cached_surf is None:
            lines = self._text.split('\n')
            width, height = self.get_size()
            line_height = self._font.get_linesize()
            surf = pygame.Surface((width, height), pygame.SRCALPHA)

            for i, line in enumerate(lines):
                text_surf = self._font.render(line, True, text_color)
                bounding = text_surf.get_bounding_rect()

                if alignment == 'left':
                    x = -bounding.x
                elif alignment == 'right':
                    x = (width - bounding.width) - bounding.x
                else:  
                    x = (width - bounding.width) // 2 - bounding.x

                y = i * line_height
                surf.blit(text_surf, (x, y))

            self._cached_surf = surf
            self._cache_key = cache_key
            self.needs_update = False

        surface.blit(self._cached_surf, rect.topleft)

        self.draw_children(surface)

class Image(UIComponent):
    def __init__(self, src: str, alt: str = "", pos: tuple[int, int] = (0, 0),
                 size: tuple[int, int] = (0, 0)):
        try:
            image_surface = pygame.image.load(src)
        except pygame.error as e:
            print(f"Failed to load image '{src}': {e}")
            image_surface = pygame.Surface(size)
            image_surface.fill((255, 0, 0))  # Fallback: red surface

        if size and size != (0, 0):
            image_surface = pygame.transform.scale(image_surface, size)
        else:
            size = image_surface.get_size()

        super().__init__(pos, size, "IMAGE", DefaultStyles.Image)
        self._name = "IMAGE"
        self.src = src
        self.alt = alt
        self.image_surface = image_surface

    def draw(self, surface):
        rect = self.get_rect()
        surface.blit(self.image_surface, rect)
        self.draw_children(surface)


class Button(UIComponent):
    """
    A clickable, stylable rectangle with centered text.
    Caches its rendered text surface and invokes a callback
    (with or without a value parameter) on click.
    """
    def __init__(self, pos=(0, 0), size=(0, 0), text="", callback=None, value=None):
        super().__init__(pos, size, "BUTTON", DefaultStyles.Button)
        self._name = "BUTTON"
        self._text = text
        self._value = value
        self.callback = callback

        self._text_cache_key = None
        self._cached_text_surf = None
        self._cached_text_rect = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def draw(self, surface):
        rect = self.get_rect()
        bg_color = self.get_style_property(StyleProperty.BACKGROUND_COLOR, self.hovered, True)
        pygame.draw.rect(surface, bg_color, rect)


        border_size = self.get_style_property(StyleProperty.BORDER_SIZE, self.hovered)
        if border_size and border_size > 0:
            border_color = self.get_style_property(StyleProperty.BORDER_COLOR, self.hovered, True)
            if(border_color):
                pygame.draw.rect(surface, border_color, rect, border_size)

        if self._text:
            text_color = self.get_style_property(StyleProperty.TEXT_COLOR, self.hovered, True)
            font = self.get_font()
            cache_key = (self._text, text_color, rect.size)
            if cache_key != self._text_cache_key:
                text_surf = font.render(self._text, True, text_color)
                text_rect = text_surf.get_rect(center=rect.center)
                self._cached_text_surf = text_surf
                self._cached_text_rect = text_rect
                self._text_cache_key = cache_key
            surface.blit(self._cached_text_surf, self._cached_text_rect)

        for child in self.children:
            child.draw(surface)

    def handle_event(self, event):
        if not self.active:
            return False
        rect = self.get_rect()

        if event.type == MOUSEMOTION:
            was_hovered = self.hovered
            self.hovered = rect.collidepoint(event.pos)
            changed = self.hovered != was_hovered
            self.propagate_event(event)
            return changed

        elif event.type == MOUSEBUTTONDOWN and self.hovered:
            if self.callback:
                signature = inspect.signature(self.callback)
                if len(signature.parameters) == 0:
                    self.callback()
                else:
                    self.callback(self._value)
            self.propagate_event(event)
            self.activate()
            return True

        self.propagate_event(event)
        return False


class DropdownItem(UIComponent):
    """
    A single entry in a dropdown list. Renders its own background,
    border, and text, and triggers its callback when clicked.
    """

    def __init__(self, pos=(0, 0), size=(0, 0), text="", callback=None):
        super().__init__(pos, size, "DROPDOWN ITEM", DefaultStyles.Dropdown)
        self._name = "DROPDOWN ITEM"
        self._text = text
        self.callback = callback
        # Cache
        self._text_cache_key = None
        self._cached_text_surf = None
        self._cached_text_rect = None

    def draw(self, surface):
        rect = self.get_rect()
        bg_color = self.get_style_property(StyleProperty.BACKGROUND_COLOR, self.hovered, True)
        border_size = self.get_style_property(StyleProperty.BORDER_SIZE, self.hovered)
        pygame.draw.rect(surface, bg_color, rect)
        if border_size:
            border_color = self.get_style_property(StyleProperty.BORDER_COLOR, self.hovered, True)
            pygame.draw.rect(surface, border_color, rect, border_size)

        text_color = self.get_style_property(StyleProperty.TEXT_COLOR, self.hovered, True)
        font = self.get_font()
        cache_key = (self._text, text_color, rect.size)
        if cache_key != self._text_cache_key:
            surf = font.render(self._text, True, text_color)
            text_rect = surf.get_rect(center=rect.center)
            self._cached_text_surf = surf
            self._cached_text_rect = text_rect
            self._text_cache_key = cache_key
        surface.blit(self._cached_text_surf, self._cached_text_rect)

    def handle_event(self, event):
        if not self.active:
            return False
        
        rect = self.get_rect()
        if event.type == MOUSEMOTION:
            was_hovered = self.hovered
            self.hovered = rect.collidepoint(event.pos)
            self.propagate_event(event)
            return self.hovered != was_hovered
        
        elif event.type == MOUSEBUTTONDOWN and self.hovered:
            if self.callback:
                self.callback()
            self.propagate_event(event)
            self.activate()
            return True
        
        self.propagate_event(event)
        return False


class Dropdown(UIComponent):
    """
    A composite component that shows the currently selected option
    and, when clicked, expands to reveal its DropdownItem children.
    Handles selection, expansion toggling, and fires back a callback
    with the chosen value.
    """

    def __init__(self, pos=(0, 0), size=(0, 0), options=None, default=0, callback=None):
        super().__init__(pos, size, "DROPDOWN", DefaultStyles.Dropdown)
        self._name = "DROPDOWN"
        self.options = options or []
        self.selected = default
        self.expanded = False
        self.callback = callback
    
        self._text_cache_key = None
        self._cached_text_surf = None
        self._cached_text_rect = None

        for i, option in enumerate(self.options):
            item_pos = (0, (i+1) * size[1])
            self.add_children([DropdownItem(item_pos, size, option, self.make_item_callback(i))])


    def make_item_callback(self, index: int):
        def callback():
            self.selected = index
            self.expanded = False

            if self.callback:
                self.callback(self.options[self.selected])
        return callback

    def draw(self, surface):
        rect = self.get_rect()
        bg_color = self.get_style_property(StyleProperty.BACKGROUND_COLOR, self.hovered, True)
        border_size = self.get_style_property(StyleProperty.BORDER_SIZE, self.hovered)
        pygame.draw.rect(surface, bg_color, rect)

        if border_size:
            border_color = self.get_style_property(StyleProperty.BORDER_COLOR, self.hovered, True)
            pygame.draw.rect(surface, border_color, rect, border_size)

        text_color = self.get_style_property(StyleProperty.TEXT_COLOR, self.hovered, True)
        font = self.get_font()
        text = self.options[self.selected]
        cache_key = (text, text_color, rect.size)
        if cache_key != self._text_cache_key:
            surf = font.render(text, True, text_color)
            text_rect = surf.get_rect(center=rect.center)
            self._cached_text_surf = surf
            self._cached_text_rect = text_rect
            self._text_cache_key = cache_key
        surface.blit(self._cached_text_surf, self._cached_text_rect)

        if self.expanded:
            self.draw_children(surface)
   

    def handle_event(self, event):
        if not self.active:
            return False, None

        rect = self.get_rect()

        if event.type == MOUSEMOTION:
            self.hovered = rect.collidepoint(event.pos)
            if self.expanded:
                self.propagate_event(event)

        elif event.type == MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                self.expanded = not self.expanded
                return True, None

            elif self.expanded:
                self.activate()
                for child in self.children:
                    if child.handle_event(event):
                        return True, self.options[self.children.index(child)]

        return False, None

    def deactivate(self):
        self.expanded = False



class Slider(UIComponent):
    """
    A track-and-thumb control for selecting a numeric value in a range.
    Draws the filled progress and draggable thumb, handles mouse drag events,
    and reports value changes via callback.
    """
    def __init__(self, pos: tuple[int, int] = (0, 0), track_size: tuple[int, int] = (0, 0),  thumb_size: tuple[int, int] = (20, 20), min: int = 0, max: int = 1, default: int = 0, callback: callable = None):
        super().__init__(pos, track_size, "SLIDER", DefaultStyles.Slider)
        self._name = "SLIDER"
        self.min = min
        self.max = max
        self.value = default
        self.dragging = False
        self.thumb_hovered = False
        self.thumb_size = thumb_size
        self._cache_key = ()
        self.callback = callback

       
    def _get_thumb_rect(self, rect: pygame.Rect):
        range_val = self.max - self.min
        if range_val == 0:
            center_x = rect.left 
        else:
            center_x = rect.left + (self.value - self.min) / range_val * rect.width
        
        thumb_x = center_x - self.thumb_size[0] / 2
        thumb_y = rect.top + (rect.height - self.thumb_size[1]) / 2
        return pygame.Rect(thumb_x, thumb_y, *self.thumb_size)
    
    def _get_progress_rect(self, rect:pygame.Rect):
        range_val = self.max - self.min
        if range_val != 0:
            progress_width = (self.value - self.min) / range_val * rect.width
        else:
            progress_width = 0  # Fallback in case range is 0
        
        return pygame.Rect(rect.left, rect.top, progress_width, rect.height)
    
    def draw(self, surface):
        rect = self.get_rect()
        thumb_rect = self._get_thumb_rect(rect)

        background_color = self.get_style_property(StyleProperty.BACKGROUND_COLOR, self.hovered, False)
        foreground_color = self.get_style_property(StyleProperty.FOREGROUND_COLOR, self.hovered, True)
        border_size = self.get_style_property(StyleProperty.BORDER_SIZE, self.hovered)
        border_color = self.get_style_property(StyleProperty.BORDER_COLOR, self.hovered, True)
        thumb_color = self.get_style_property(StyleProperty.THUMB_COLOR, self.thumb_hovered, True)

        pygame.draw.rect(surface, background_color, rect)
        if border_size > 0:
            pygame.draw.rect(surface, border_color, rect, border_size)
        
        if foreground_color != None:
            progress_rect = self._get_progress_rect(rect)
            pygame.draw.rect(surface, foreground_color, progress_rect)

        pygame.draw.rect(surface, thumb_color, thumb_rect)

    def handle_event(self, event):
        rect = self.get_rect()
        
        if event.type == MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                self.dragging = True
                self.thumb_hovered = True
                self.hovered = True

        elif event.type == MOUSEBUTTONUP:
            self.dragging = False


        if event.type == MOUSEMOTION and self.dragging == False:
            thumb_rect = self._get_thumb_rect(rect)
            self.thumb_hovered = thumb_rect.collidepoint(event.pos)

            if(self.thumb_hovered == False):
                self.hovered = rect.collidepoint(event.pos)

            else:
                self.hovered = True
                
            
        if self.dragging:
            pos_x = event.pos[0]
            if pos_x:
                x = max(rect.left, min(event.pos[0], rect.right))
                self.value = self.min + (x - rect.left) / rect.width * (self.max - self.min)
                if hasattr(self, 'step'):
                    self.value = round(self.value / self.step) * self.step
                if self.callback:
                    self.callback(self.value)
                return True
        
        self.propagate_event(event)
        return False
