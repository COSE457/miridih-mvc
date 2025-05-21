from typing import List, Optional
from .base_shape import BaseShape

class Canvas:
    _instance = None
    
    def __new__(cls):
        """싱글톤 패턴 구현"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.shapes = []
            cls._instance.selected_shapes = []
            cls._instance.observers = []
        return cls._instance
    
    def add_shape(self, shape: BaseShape) -> None:
        """도형 추가"""
        self.shapes.append(shape)
        self.notify_observers()
    
    def remove_shape(self, shape: BaseShape) -> None:
        """도형 제거"""
        if shape in self.shapes:
            self.shapes.remove(shape)
            if shape in self.selected_shapes:
                self.selected_shapes.remove(shape)
            self.notify_observers()
    
    def get_shapes(self) -> List[BaseShape]:
        """z-order 기준으로 정렬된 도형 목록 반환"""
        return sorted(self.shapes, key=lambda x: x.z_order)
    
    def select_shapes(self, shapes: List[BaseShape]) -> None:
        """도형 선택 여부 (True/False) 변경"""
        for shape in self.selected_shapes:
            shape.selected = False
        self.selected_shapes = shapes
        for shape in shapes:
            shape.selected = True
        self.notify_observers()
    
    def add_observer(self, observer) -> None:
        """옵저버 등록"""
        if observer not in self.observers:
            self.observers.append(observer)
    
    def notify_observers(self) -> None:
        """옵저버 변경사항 알림"""
        for observer in self.observers:
            observer.update() 