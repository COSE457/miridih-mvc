from .shapes.rectangle import Rectangle
from .shapes.ellipse import Ellipse
from .shapes.line import Line
from .shapes.text import Text
from .shapes.image import Image

class ShapeFactory:
    """
    Factory class for creating different types of shapes.
    Provides a centralized way to create shape instances.
    """
    
    @staticmethod
    def create_shape(shape_type: str, x: int = 0, y: int = 0, text: str = None, image_path: str = None):
        """
        Create a new shape instance.
        
        Args:
            shape_type: Type of shape to create
            x: X coordinate (for text and image)
            y: Y coordinate (for text and image)
            text: Text content (for text shape)
            image_path: Path to image file (for image shape)
            
        Returns:
            New shape instance
            
        Raises:
            ValueError: If shape type is unknown or required parameters are missing
        """
        shape_types = {
            "rectangle": Rectangle,
            "ellipse": Ellipse,
            "line": Line,
            "text": Text,
            "image": Image
        }
        
        shape_class = shape_types.get(shape_type.lower())
        if not shape_class:
            raise ValueError(f"Unknown shape type: {shape_type}")
        
        if shape_type == "text":
            if text is None:
                raise ValueError("Text shape requires a 'text' argument")
            return shape_class(x, y, text)
        elif shape_type == "image":
            if image_path is None:
                raise ValueError("Image shape requires an 'image_path' argument")
            return shape_class(x, y, image_path)
        else:
            return shape_class()  # No arguments for rectangle, ellipse, line