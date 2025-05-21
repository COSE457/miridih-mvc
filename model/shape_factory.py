from .shapes.rectangle import Rectangle
from .shapes.ellipse import Ellipse
from .shapes.line import Line
from .shapes.text import Text
from .shapes.image import Image

class ShapeFactory:
    """
    도형 생성을 위한 팩토리 클래스
    """
    
    @staticmethod
    def create_shape(shape_type: str, x: int = 0, y: int = 0, text: str = None, image_path: str = None):
        """
        도형 인스턴스 생성
        
        Args:
            shape_type: 생성할 도형 타입
            x: X 좌표 (텍스트, 이미지용)
            y: Y 좌표 (텍스트, 이미지용)
            text: 텍스트 내용 (텍스트 도형용)
            image_path: 이미지 파일 경로 (이미지 도형용)
            
        Returns:
            새로운 도형 인스턴스
            
        Raises:
            ValueError: 알 수 없는 도형 타입이거나 필수 args가 누락된 경우
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
            return shape_class()