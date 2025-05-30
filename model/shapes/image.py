from typing import Dict, Any
from ..base_shape import BaseShape

class Image(BaseShape):
    """이미지 생성"""
    
    def __init__(self, x: int, y: int, image_path: str, width: int = 200, height: int = 200):
        super().__init__()
        self.x = x
        self.y = y
        self.image_path = image_path
        self.width = width
        self.height = height
        self.has_shadow = False
        self.has_frame = False
        self.z_order = 0
        self.selected = False
    
    def draw(self) -> Dict[str, Any]:
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
    
    def set_property(self, property_name: str, value: Any) -> None:
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