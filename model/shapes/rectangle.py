from typing import Dict, Any
from ..base_shape import BaseShape

class Rectangle(BaseShape):
    """사각형 생성"""
    
    def __init__(self):
        super().__init__()
        self.shape_type = "rectangle"
    
    def draw(self) -> Dict[str, Any]:

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