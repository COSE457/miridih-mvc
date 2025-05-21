from abc import ABC, abstractmethod
from typing import Dict, Any
import uuid

class BaseShape(ABC):
    """
    모든 도형의 기본 클래스
    """
    
    def __init__(self):
        """기본 도형 속성 init"""
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
        """도형 생성 및 도형 속성 반환"""
        pass
    
    def set_property(self, name: str, value: Any) -> None:
        """
        도형의 속성 설정
        """
        if hasattr(self, name):
            setattr(self, name, value)
    
    def get_property(self, name: str) -> Any:
        """
        도형 속성 반환
        """
        return getattr(self, name, None)
    
    def move(self, dx: int, dy: int) -> None:
        """
        도형 이동
        """
        self.x += dx
        self.y += dy
    
    def resize(self, dw: int, dh: int) -> None:
        """
        도형 사이즈 조정
        """
        self.width = max(10, self.width + dw)
        self.height = max(10, self.height + dh) 