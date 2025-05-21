from typing import Dict, Any
from ..base_shape import BaseShape

class Line(BaseShape):
    """Line shape implementation."""
    
    def __init__(self):
        """Initialize line shape."""
        super().__init__()
        self.shape_type = "line"
        self.x2 = 0  # End point x
        self.y2 = 0  # End point y
        self.width = 1  # Line width
    
    def draw(self) -> Dict[str, Any]:
        """
        Draw the line and return its properties.
        
        Returns:
            Dict containing line properties
        """
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
    
    def resize(self, dw: int, dh: int) -> None:
        """
        Resize the line by updating its end point.
        
        Args:
            dw: Change in x2
            dh: Change in y2
        """
        self.x2 += dw
        self.y2 += dh 