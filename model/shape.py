import tkinter as tk
from tkinter import PhotoImage, filedialog, simpledialog
from abc import ABC, abstractmethod
from typing import Dict, Callable, Optional, List, Union
import os
import uuid

class Shape(ABC):
    # 기본값
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.x = 0
        self.y = 0
        self.width = 100
        self.height = 100
        self.text = ""
        self.z_order = 0
        self.has_frame = False
        self.has_shadow = False
        self.selected = False
        self.fill = ""
        self.outline = "black"
        
    @abstractmethod
    def draw(self) -> Dict:
        pass
    
    def set_property(self, name: str, value: any) -> None:
        if hasattr(self, name):
            setattr(self, name, value)
    
    def get_property(self, name: str) -> any:
        return getattr(self, name, None)
    
    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy
    
    def resize(self, dw: int, dh: int) -> None:
        self.width = max(10, self.width + dw)
        self.height = max(10, self.height + dh)

class Rectangle(Shape):
    def __init__(self):
        super().__init__()
        self.shape_type = "rectangle"
        
    def draw(self) -> Dict:
        return {
            'type': self.shape_type,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'text': self.text,
            'z_order': self.z_order,
            'has_frame': self.has_frame,
            'has_shadow': self.has_shadow,
            'selected': self.selected,
            'fill': self.fill,
            'outline': self.outline
        }

class Ellipse(Shape):
    def __init__(self):
        super().__init__()
        self.shape_type = "ellipse"
        
    def draw(self) -> Dict:
        return {
            'type': self.shape_type,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'text': self.text,
            'z_order': self.z_order,
            'has_frame': self.has_frame,
            'has_shadow': self.has_shadow,
            'selected': self.selected,
            'fill': self.fill,
            'outline': self.outline
        }

class Line(Shape):
    def __init__(self):
        super().__init__()
        self.shape_type = "line"
        self.x2 = 0  # End point x
        self.y2 = 0  # End point y
        self.width = 1  # Line width
        
    def draw(self) -> Dict:
        return {
            'type': self.shape_type,
            'x': self.x,
            'y': self.y,
            'x2': self.x2,
            'y2': self.y2,
            'width': self.width,
            'z_order': self.z_order,
            'selected': self.selected,
            'outline': self.outline
        }
        
class Text(Shape):  # Inherit from Shape if applicable
    def __init__(self, x: int, y: int, text: str, width: int = 100, height: int = 30):
        super().__init__()  # Call base class __init__ if inheriting
        self.x = x
        self.y = y
        self.text = text
        self.font = "Arial"
        self.font_size = 12
        self.text_color = "black"
        self.width = width
        self.height = height
        self.z_order = 0
        self.selected = False

    def draw(self) -> Dict:
        return {
            'type': 'text',
            'x': self.x,
            'y': self.y,
            'text': self.text,
            'font': self.font,
            'font_size': self.font_size,
            'text_color': self.text_color,
            'z_order': self.z_order,
            'selected': self.selected,
            'width': self.width,
            'height': self.height
        }

    def set_property(self, property_name: str, value):
        if property_name == 'text':
            self.text = value
        elif property_name == 'font':
            self.font = value
        elif property_name == 'font_size':
            self.font_size = int(value)
        elif property_name == 'text_color':
            self.text_color = value
        elif property_name in ['x', 'y', 'width', 'height', 'z_order']:
            setattr(self, property_name, int(value))
        elif property_name == 'selected':
            self.selected = value
            

class Image:
    def __init__(self, x: int, y: int, image_path: str, width: int = 200, height: int = 200):
        self.id = str(uuid.uuid4())
        self.x = x
        self.y = y
        self.image_path = image_path
        self.width = width
        self.height = height
        self.has_shadow = False
        self.has_frame = False
        self.z_order = 0
        self.selected = False

    def draw(self) -> Dict:
        return {
            'type': 'image',
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'image_path': self.image_path,
            'has_shadow': self.has_shadow,
            'has_frame': self.has_frame,
            'z_order': self.z_order,
            'selected': self.selected
        }

    def set_property(self, property_name: str, value):
        if property_name == 'image_path':
            self.image_path = value
        elif property_name == 'has_shadow':
            self.has_shadow = value
        elif property_name == 'has_frame':
            self.has_frame = value
        elif property_name in ['x', 'y', 'width', 'height', 'z_order']:
            setattr(self, property_name, int(value))
        elif property_name == 'selected':
            self.selected = value
