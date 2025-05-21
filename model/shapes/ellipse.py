from typing import Dict, Any
from ..base_shape import BaseShape

class Ellipse(BaseShape):
    """Ellipse shape implementation."""
    
    def __init__(self):
        """Initialize ellipse shape."""
        super().__init__()
        self.shape_type = "ellipse"
    
    def draw(self) -> Dict[str, Any]:
        """
        Draw the ellipse and return its properties.
        
        Returns:
            Dict containing ellipse properties
        """
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