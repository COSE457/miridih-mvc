from abc import ABC, abstractmethod
from typing import Dict, Any
import uuid

class BaseShape(ABC):
    """
    Abstract base class for all shapes in the application.
    Defines common properties and methods for all shapes.
    """
    
    def __init__(self):
        """Initialize common shape properties."""
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
    def draw(self) -> Dict[str, Any]:
        """
        Draw the shape and return its properties.
        
        Returns:
            Dict containing shape properties for drawing
        """
        pass
    
    def set_property(self, name: str, value: Any) -> None:
        """
        Set a property of the shape.
        
        Args:
            name: Name of the property
            value: Value to set
        """
        if hasattr(self, name):
            setattr(self, name, value)
    
    def get_property(self, name: str) -> Any:
        """
        Get a property of the shape.
        
        Args:
            name: Name of the property
            
        Returns:
            Value of the property
        """
        return getattr(self, name, None)
    
    def move(self, dx: int, dy: int) -> None:
        """
        Move the shape by the given delta.
        
        Args:
            dx: Change in x position
            dy: Change in y position
        """
        self.x += dx
        self.y += dy
    
    def resize(self, dw: int, dh: int) -> None:
        """
        Resize the shape by the given delta.
        
        Args:
            dw: Change in width
            dh: Change in height
        """
        self.width = max(10, self.width + dw)
        self.height = max(10, self.height + dh) 