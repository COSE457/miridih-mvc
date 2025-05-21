from typing import Dict, Any
from ..base_shape import BaseShape

class Line(BaseShape):
    """선 생성"""
    
    def __init__(self):
        super().__init__()
        self.shape_type = "line"
        self.x2 = 0  # x 좌표
        self.y2 = 0  # y 좌표
        self.width = 1  # 선 두꼐 조절 (기본값 변경 필요 시 코드 수정)
    
    def draw(self) -> Dict[str, Any]:

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
        기본 resize 함수를 override하여 선의 끝점을 조정
        """
        self.x2 += dw
        self.y2 += dh 