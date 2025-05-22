from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class ShapeComponent(ABC):
    @abstractmethod
    def draw(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def is_point_inside(self, x: float, y: float) -> bool:
        pass
    
    @abstractmethod
    def move(self, dx: float, dy: float):
        pass
    
    @abstractmethod
    def get_bounds(self) -> tuple:
        pass

class ShapeGroup(ShapeComponent):
    def __init__(self):
        self.shapes: List[ShapeComponent] = []
        self.selected = False
    
    def add(self, shape: ShapeComponent):
        self.shapes.append(shape)
    
    def remove(self, shape: ShapeComponent):
        self.shapes.remove(shape)
    
    def draw(self) -> Dict[str, Any]:
        # Draw all shapes in the group
        for shape in self.shapes:
            shape.draw()
        
        # Return group properties
        return {
            'type': 'group',
            'selected': self.selected,
            'shapes': self.shapes
        }
    
    def is_point_inside(self, x: float, y: float) -> bool:
        return any(shape.is_point_inside(x, y) for shape in self.shapes)
    
    def move(self, dx: float, dy: float):
        for shape in self.shapes:
            shape.move(dx, dy)
    
    def get_bounds(self) -> tuple:
        if not self.shapes:
            return (0, 0, 0, 0)
        
        # Get bounds of all shapes
        bounds = [shape.get_bounds() for shape in self.shapes]
        min_x = min(b[0] for b in bounds)
        min_y = min(b[1] for b in bounds)
        max_x = max(b[2] for b in bounds)
        max_y = max(b[3] for b in bounds)
        
        return (min_x, min_y, max_x, max_y)
    
    def select(self):
        self.selected = True
        for shape in self.shapes:
            shape.selected = True
    
    def deselect(self):
        self.selected = False
        for shape in self.shapes:
            shape.selected = False 