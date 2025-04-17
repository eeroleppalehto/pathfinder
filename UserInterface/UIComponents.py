from __future__ import annotations
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP
from .UIStyles import Styleable, ComponentStyleManager, StyleSheet 
from .UIStyles import StyleGroup, StyleProperty, StyleType 
from .UIDefaultStyles import DefaultStyles
from .UIManager import UIRoot

import pygame

"""
        events are currently handled in a really dumb way, 
        events should bubble up and stop propropagating after we have found the element that we are intersecting with
        deepest leaf node on(one of the childrens children) is the top most drawn element, if we bubble up and we 
        intersect with an elment, it means that we are intersecting with the top most visible element,
        then we should stop handling the events(stop propropagating)
"""

pygame.init()

class UIComponent(Styleable):
    def __init__(self, position: tuple[int, int], size: tuple[int, int], style_group: StyleGroup):
        self._local_position = position  
        self._size = size
        self.active = True
        self.hovered = False
        self.children: list[UIComponent] = []
        self.style_manager = ComponentStyleManager(style_group)
        self.style = style_group.normal
        self.hover_style = style_group.hover
        self.parent: UIComponent | None = None
        self.root: UIRoot | None = None

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
        self.style_manager.set_normal_style(style)
        for child in self.children:
            child.style_manager.set_normal_style(style)

    def set_hover_style(self, style: StyleSheet):
        self.style_manager.set_hover_style(style)
        for child in self.children:
            child.style_manager.set_hover_style(style)

    def get_style_property(self, property: StyleProperty, is_hovered: bool):
        return self.style_manager.get_resolved_property(property, is_hovered)
        
    def set_style_property(self, property: StyleProperty, value, state: int = StyleType.NORMAL):
        self.style_manager.set_override(property, value, state)

    def get_font(self) -> pygame.font.Font | None:
        return self.style_manager.get_resolved_font(self.hovered)

    def get_active_style(self):
        return self.hover_style if self.hovered else self.style

    def draw_children(self, surface):
        for child in self.children:
            child.draw(surface)

    """probably should bubble up from the last element in the tree"""
    def propagate_event(self, event):
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
    def __init__(self, position: tuple[int, int] = (0, 0), size: tuple[int, int] = (0, 0), callback: callable = None):
        super().__init__(position, size, DefaultStyles.Panel)
        self.callback = callback
  
    def draw(self, surface):
        rect = self.get_rect()
        background_color = self.get_style_property(StyleProperty.BACKGROUND_COLOR, self.hovered)
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
    def __init__(self, position: tuple[int, int], text: str):
        super().__init__(position, (0, 0), DefaultStyles.Header)
        self.text = text
        self._font = self.style.get_font()
        self.update_size()

    def set_text_content(self, text: str):
        """Update text and recalculate size."""
        self.text = text
        self.update_size()

    def update_size(self):
        """Calculate size for multiline text without padding."""
        lines = self.text.split('\n') if self.text else ['']
        max_width = 0
        line_height = self._font.get_linesize()
        for line in lines:
            w, _ = self._font.size(line)
            max_width = max(max_width, w)
        total_height = line_height * len(lines)
        self.set_size(max_width, total_height)

    def draw(self, surface):
        rect = self.get_rect()
        bg_color = self.get_style_property(StyleProperty.BACKGROUND_COLOR, self.hovered)
        text_color = self.get_style_property(StyleProperty.TEXT_COLOR, self.hovered)
        alignment = self.get_style_property(StyleProperty.TEXT_ALIGN, self.hovered) or 'left'

        # Draw background
        if bg_color is not None:
            pygame.draw.rect(surface, bg_color, rect)

        # Prepare multiline rendering
        lines = self.text.split('\n') if self.text else ['']
        line_height = self._font.get_linesize()
        total_h = line_height * len(lines)
        # Vertical centering
        start_y = rect.top + (rect.height - total_h) // 2

        for i, line in enumerate(lines):
            text_surf = self._font.render(line, True, text_color)
            text_rect = text_surf.get_rect()
            # Horizontal alignment without padding or margin
            if alignment == 'left':
                text_rect.x = rect.left
            elif alignment == 'right':
                text_rect.x = rect.right - text_rect.width
            else:  # center
                text_rect.x = rect.left + (rect.width - text_rect.width) // 2
            # Vertical position
            text_rect.y = start_y + i * line_height
            surface.blit(text_surf, text_rect)

        self.draw_children(surface)

class Image(UIComponent):
    def __init__(self, src: str, alt: str = "", position: tuple[int, int] = (0, 0),
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

        super().__init__(position, size, DefaultStyles.Image)
        self.src = src
        self.alt = alt
        self.image_surface = image_surface

    def draw(self, surface):
        rect = self.get_rect()
        surface.blit(self.image_surface, rect)
        self.draw_children(surface)


class Button(UIComponent):
    def __init__(self, position: tuple[int, int] = (0, 0), size: tuple[int, int] = (0, 0), text: str = "", callback: callable = None):
        super().__init__(position, size, DefaultStyles.Button)
        self.text = text
        self.callback = callback

    def draw(self, surface):
        rect = self.get_rect()
        background_color = self.get_style_property(StyleProperty.BACKGROUND_COLOR, self.hovered)
        
        pygame.draw.rect(surface, background_color, rect)

        if self.text != None and len(self.text) > 0:
            text_color = self.get_style_property(StyleProperty.TEXT_COLOR, self.hovered)
            font:pygame.font.Font = self.get_font()
            text_surf = font.render(self.text, True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect)
            
        self.draw_children(surface)

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
                self.callback()
            self.propagate_event(event)
            self.activate()
            return True

        self.propagate_event(event)
        return False


class DropdownItem(UIComponent):
    def __init__(self, position: tuple[int, int] = (0, 0), size: tuple[int, int] = (0, 0),text: str = "", callback: callable = None):
        super().__init__(position, size, DefaultStyles.Dropdown)
        self.text = text
        self.callback = callback

    def draw(self, surface):
        rect = self.get_rect()

        background_color = self.get_style_property(StyleProperty.BACKGROUND_COLOR, self.hovered)
        border_size = self.get_style_property(StyleProperty.BORDER_SIZE, self.hovered)
        text_color = self.get_style_property(StyleProperty.TEXT_COLOR, self.hovered)

        pygame.draw.rect(surface, background_color, rect)
        if border_size > 0:
            border_color = self.get_style_property(StyleProperty.BORDER_COLOR, self.hovered)
            pygame.draw.rect(surface, border_color, rect, border_size)

        font = self.get_font()
        text_surf = font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

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
    def __init__(self, position: tuple[int, int] = (0, 0), size: tuple[int, int] = (0, 0),options: list[str] = [], default=0, callback: callable = None):
        super().__init__(position, size, DefaultStyles.Dropdown)
        self.options = options
        self.selected = default
        self.expanded = False
        self.callback = callback

        for i, option in enumerate(options):
            item_position = (0, (i + 1) * size[1])
            item = DropdownItem(item_position, size, option, self.make_item_callback(i))
            self.add_children([item])

    def make_item_callback(self, index: int):
        def callback():
            self.selected = index
            self.expanded = False

            if self.callback:
                self.callback(self.options[self.selected])
        return callback

    def draw(self, surface):
        rect = self.get_rect()
        background_color = self.get_style_property(StyleProperty.BACKGROUND_COLOR, self.hovered)
        border_size = self.get_style_property(StyleProperty.BORDER_SIZE, self.hovered)
        text_color = self.get_style_property(StyleProperty.TEXT_COLOR, self.hovered)
        
        pygame.draw.rect(surface, background_color, rect)
        if border_size > 0:
            border_color = self.get_style_property(StyleProperty.BORDER_COLOR, self.hovered)
            pygame.draw.rect(surface, border_color, rect, border_size)

        font = self.get_font()
        text_surf = font.render(self.options[self.selected], True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

        if self.expanded:
            for child in self.children:
                child.draw(surface)

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
    def __init__(self, position: tuple[int, int] = (0, 0), track_size: tuple[int, int] = (0, 0),  thumb_size: tuple[int, int] = (20, 20), min: int = 0, max: int = 1, default: int = 0, callback: callable = None):
        super().__init__(position, track_size, DefaultStyles.Slider)
        self.min = min
        self.max = max
        self.value = default
        self.dragging = False
        self.thumb_hovered = False
        self.thumb_size = thumb_size
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
        thumb_hovered = thumb_rect.collidepoint(pygame.mouse.get_pos())

        background_color = self.get_style_property(StyleProperty.BACKGROUND_COLOR, self.hovered)
        foreground_color = self.get_style_property(StyleProperty.FOREGROUND_COLOR, self.hovered)
        border_size = self.get_style_property(StyleProperty.BORDER_SIZE, self.hovered)
        border_color = self.get_style_property(StyleProperty.BORDER_COLOR, self.hovered)
        thumb_color = self.get_style_property(StyleProperty.SLIDER_THUMB_COLOR, thumb_hovered)

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

        elif event.type == MOUSEBUTTONUP:
            self.dragging = False

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
