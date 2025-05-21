from typing import Dict, Any
from ..base_shape import BaseShape

class Text(BaseShape):
    """텍스트 생성"""
    
    def __init__(self, x: int, y: int, text: str, width: int = 100, height: int = 30):
        super().__init__()
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
    
    def draw(self) -> Dict[str, Any]:

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
    
    def set_property(self, property_name: str, value: Any) -> None:
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