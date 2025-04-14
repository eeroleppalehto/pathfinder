from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP
import pygame


class UIColors:
    PANEL_BG = (217, 217, 217)
    WINDOW_BG = (224, 224, 224)
    CANVAS_BG = (240, 240, 240)
    BUTTON_TEXT = (255, 255, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

class UIComponent:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self.active = True

    def get_position(self):
        return (self._x, self._y)

    def set_position(self, x, y):
        self._x = x
        self._y = y

    def get_size(self):
        return (self._width, self._height)

    def set_size(self, width, height):
        self._width = width
        self._height = height

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._width, self._height)

class Button(UIComponent):
    def __init__(self, x, y, width, height, text, callback):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False

    def draw(self, surface):
        rect = self.get_rect()
        color = (100, 100, 100) if self.hovered else (150, 150, 150)
        pygame.draw.rect(surface, color, rect)
        font = pygame.font.Font(None, 24)
        text_surf = font.render(self.text, True, UIColors.WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if not self.active:
            return False
        rect = self.get_rect()
        if event.type == MOUSEMOTION:
            self.hovered = rect.collidepoint(event.pos)
        elif event.type == MOUSEBUTTONDOWN and self.hovered:
            self.callback()
            return True
        return False

class IconButton(Button):
    def __init__(self, x, y, width, height, text, callback, icon_color):
        super().__init__(x, y, width, height, text, callback)
        self.icon_color = icon_color
        self.base_color = (150, 150, 150)
        self.selected = False
    
    def draw(self, surface):
        rect = self.get_rect()
        bg_color = (100, 100, 100) if self.hovered else self.base_color
        pygame.draw.rect(surface, bg_color, rect)
        icon = pygame.Rect(self._x + (self._width//2 - self._height//4), self._y + (self._height//2 - self._height//4), self._height//2, self._height//2)
        pygame.draw.rect(surface, self.icon_color, icon)
    
    def activate(self):
        self.selected = True
        self.base_color = (100, 100, 100)

    def deactivate(self):
        self.selected = False
        self.base_color = (150, 150, 150)
    

class DrawOptionButtonGroup:
    def __init__(self, app, x, y, button_width = 100, button_height = 30):
        self.app = app
        self.draw_wall_button = IconButton(x + 20, y, button_width//2, button_height, "Wall", self.app.set_draw_walls, UIColors.BLACK)
        self.remove_wall_button = IconButton(x + 20 + 55, y, button_width//2, button_height, "Remove", self.app.set_remove_walls, UIColors.WHITE)
        self.set_start_button = IconButton(x + 20 + 110, y, button_width//2, button_height, "Start", self.app.set_place_start, UIColors.GREEN)
        self.set_end_button = IconButton(x + 20 + 165, y, button_width//2, button_height, "End", self.app.set_place_end, UIColors.RED)
    
    def handle_event(self, event):
        if self.draw_wall_button.handle_event(event):
            self.deactivate_all()
            self.draw_wall_button.activate()
        elif self.remove_wall_button.handle_event(event):
            self.deactivate_all()
            self.remove_wall_button.activate()
        elif self.set_start_button.handle_event(event):
            self.deactivate_all()
            self.set_start_button.activate()
        elif self.set_end_button.handle_event(event):
            self.deactivate_all()
            self.set_end_button.activate()
    
    def draw(self, surface):
        self.draw_wall_button.draw(surface)
        self.remove_wall_button.draw(surface)
        self.set_start_button.draw(surface)
        self.set_end_button.draw(surface)

    def deactivate_all(self):
        self.draw_wall_button.deactivate()
        self.remove_wall_button.deactivate()
        self.set_start_button.deactivate()
        self.set_end_button.deactivate()
    
    def hide():...

class Dropdown(UIComponent):
    def __init__(self, x, y, width, height, options, default=0):
        super().__init__(x, y, width, height)
        self.options = options
        self.selected = default
        self.expanded = False

    def draw(self, surface):
        rect = self.get_rect()
        pygame.draw.rect(surface, UIColors.WHITE, rect)
        pygame.draw.rect(surface, UIColors.WHITE, rect, 1)
        font = pygame.font.Font(None, 24)
        text_surf = font.render(self.options[self.selected], True, UIColors.BLACK)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

        if self.expanded:
            for i, option in enumerate(self.options):
                item_rect = pygame.Rect(
                    rect.x, 
                    rect.y + (i + 1) * rect.height,
                    rect.width, 
                    rect.height
                )
                pygame.draw.rect(surface, UIColors.WHITE, item_rect)
                pygame.draw.rect(surface, UIColors.BLACK, item_rect, 1)
                text_surf = font.render(option, True, UIColors.BLACK)
                text_rect = text_surf.get_rect(center=item_rect.center)
                surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if not self.active:
            return False, None
        rect = self.get_rect()
        if event.type == MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                self.expanded = not self.expanded
                return True, None
            elif self.expanded:
                for i in range(len(self.options)):
                    item_rect = pygame.Rect(
                        rect.x, 
                        rect.y + (i + 1) * rect.height,
                        rect.width, 
                        rect.height
                    )
                    if item_rect.collidepoint(event.pos):
                        self.selected = i
                        self.expanded = False
                        return True, self.options[i]
        return False, None

class Slider(UIComponent):
    def __init__(self, x, y, width, height, min_val, max_val, default):
        super().__init__(x, y, width, height)
        self.min = min_val
        self.max = max_val
        self.value = default
        self.dragging = False

    def draw(self, surface):
        rect = self.get_rect()
        pygame.draw.rect(surface, UIColors.WHITE, rect)
        pygame.draw.rect(surface, UIColors.BLACK, rect, 1)
        pos = rect.left + (self.value - self.min) / (self.max - self.min) * rect.width
        thumb_rect = pygame.Rect(pos - 5, rect.top - 5, 10, rect.height + 10)
        pygame.draw.rect(surface, (100, 100, 100), thumb_rect)

    def handle_event(self, event):
        rect = self.get_rect()
        if event.type == MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == MOUSEMOTION and self.dragging:
            x = max(rect.left, min(event.pos[0], rect.right))
            self.value = self.min + (x - rect.left) / rect.width * (self.max - self.min)
            # Optional: Round to nearest integer for discrete steps
            if hasattr(self, 'step'):
                self.value = round(self.value / self.step) * self.step
            return True
        return False
