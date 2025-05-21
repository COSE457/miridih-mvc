from model.canvas import Canvas
from model.shape_factory import ShapeFactory

class CanvasController:
    
    def __init__(self, canvas_view, property_panel):
        """
        기본값
        """
        self.canvas = Canvas()
        self.canvas_view = canvas_view
        self.property_panel = property_panel
        self.canvas.add_observer(self)
        self.canvas_view.set_shape_selected_callback(self.on_canvas_click)
        self.canvas_view.set_shape_created_callback(self.on_shape_created)
        self.canvas_view.set_shape_drag_callback(self.on_shape_drag)
        self.property_panel.set_property_changed_callback(self.on_property_changed)
    
    def on_canvas_click(self, x: int, y: int, multi_select: bool = False, check_only: bool = False):
        clicked_shape = None
        for shape in reversed(self.canvas.get_shapes()):
            if (shape.x <= x <= shape.x + shape.width and
                shape.y <= y <= shape.y + shape.height):
                clicked_shape = shape
                break
        
        # shape 선택 여부 확인 용도
        if check_only:
            if clicked_shape and clicked_shape in self.canvas.selected_shapes:
                return {'is_selected': True, 'shape': clicked_shape}
            return {'is_selected': False}
        
        if clicked_shape:
            if multi_select:
                # Add to or remove from selection
                if clicked_shape in self.canvas.selected_shapes:
                    self.canvas.selected_shapes.remove(clicked_shape)
                    clicked_shape.selected = False
                else:
                    self.canvas.selected_shapes.append(clicked_shape)
                    clicked_shape.selected = True
                self.canvas.notify_observers()
            else:
                # Single selection
                self.canvas.select_shapes([clicked_shape])
            
            if len(self.canvas.selected_shapes) == 1:
                self.property_panel.update_properties(clicked_shape.draw())
            elif len(self.canvas.selected_shapes) > 1:
                # Show common properties for multiple selected shapes
                self.property_panel.show_multi_select_properties()
        elif not multi_select:
            self.canvas.select_shapes([])
            self.property_panel.clear_properties()
    

    def on_shape_drag(self, dx: int, dy: int):
        # 선택된 도형들을 dx, dy 만큼 이동
        for shape in self.canvas.selected_shapes:
            shape.move(dx, dy)
        
        # 선택된 도형이 1개인 경우 속성 패널 업데이트
        if len(self.canvas.selected_shapes) == 1:
            self.property_panel.update_properties(self.canvas.selected_shapes[0].draw())
        
        # 캔버스 다시 그리기
        self.canvas.notify_observers()
    
    def on_shape_created(self, x: int, y: int, width: int, height: int, shape_type: str = "rectangle", props: dict = None):
        if shape_type == "text" and props and 'text' in props:
            # 텍스트 도형 생성
            shape = ShapeFactory.create_shape(shape_type, x=x, y=y, text=props['text'])
            # 현재 폰트 설정 적용
            shape.font = self.property_panel.font_var.get()
            shape.font_size = int(self.property_panel.font_size_var.get())
            shape.text_color = self.property_panel.color_var.get()
        elif shape_type == "image" and props and 'image_path' in props:
            # 이미지 도형 생성
            shape = ShapeFactory.create_shape(shape_type, x=x, y=y, image_path=props['image_path'])
        else:
            # 기타 도형 생성
            shape = ShapeFactory.create_shape(shape_type)
        
        # 위치와 크기 설정 (텍스트와 이미지는 create_shape에서 설정됨)
        if shape_type not in ["text", "image"]:
            shape.x = x
            shape.y = y
        if shape_type == "line":
            shape.x2 = width
            shape.y2 = height 
        else:
            shape.width = width
            shape.height = height
        
        if props:
            for key, value in props.items():
                if key not in ['text', 'image_path']:  # Skip text/image_path since they're set
                    shape.set_property(key, value)
        
        self.canvas.add_shape(shape)
    
    def on_property_changed(self, property_name: str, value: any):
        for shape in self.canvas.selected_shapes:
            if property_name in ['x', 'y', 'width', 'height', 'z_order']:
                try:
                    value = int(value)
                except ValueError:
                    return
            shape.set_property(property_name, value)
        self.canvas.notify_observers()
    
    def update(self):
        self.canvas_view.draw_shapes(self.canvas.get_shapes())
        
    # Z-order control methods
    def bring_to_front(self):
        """Move selected shapes to the front (highest z-order)"""
        if not self.canvas.selected_shapes:
            return
            
        # Find the highest z-order value
        max_z = max(shape.z_order for shape in self.canvas.get_shapes())
        
        # Set selected shapes to have higher z-order values
        for i, shape in enumerate(self.canvas.selected_shapes):
            shape.z_order = max_z + 1 + i
            
        # Update property panel if a single shape is selected
        if len(self.canvas.selected_shapes) == 1:
            self.property_panel.update_properties(self.canvas.selected_shapes[0].draw())
            
        self.canvas.notify_observers()
    
    def send_to_back(self):
        """Move selected shapes to the back (lowest z-order)"""
        if not self.canvas.selected_shapes:
            return
            
        # Find the lowest z-order value
        min_z = min(shape.z_order for shape in self.canvas.get_shapes())
        
        # Set selected shapes to have lower z-order values
        for i, shape in enumerate(self.canvas.selected_shapes):
            shape.z_order = min_z - 1 - i
            
        # Update property panel if a single shape is selected
        if len(self.canvas.selected_shapes) == 1:
            self.property_panel.update_properties(self.canvas.selected_shapes[0].draw())
            
        self.canvas.notify_observers()
    
    def bring_forward(self):
        """Move selected shapes one level forward in z-order"""
        if not self.canvas.selected_shapes:
            return
            
        # Get all shapes sorted by z-order
        all_shapes = self.canvas.get_shapes()
        
        for selected_shape in self.canvas.selected_shapes:
            # Find the shape's index in the sorted list
            idx = next((i for i, s in enumerate(all_shapes) if s.id == selected_shape.id), -1)
            if idx < len(all_shapes) - 1:
                # Swap z-order with the next shape
                next_shape = all_shapes[idx + 1]
                temp_z = selected_shape.z_order
                selected_shape.z_order = next_shape.z_order
                next_shape.z_order = temp_z
        
        # Update property panel if a single shape is selected
        if len(self.canvas.selected_shapes) == 1:
            self.property_panel.update_properties(self.canvas.selected_shapes[0].draw())
            
        self.canvas.notify_observers()
    
    def send_backward(self):
        """Move selected shapes one level backward in z-order"""
        if not self.canvas.selected_shapes:
            return
            
        # Get all shapes sorted by z-order
        all_shapes = self.canvas.get_shapes()
        
        for selected_shape in self.canvas.selected_shapes:
            # Find the shape's index in the sorted list
            idx = next((i for i, s in enumerate(all_shapes) if s.id == selected_shape.id), -1)
            if idx > 0:
                # Swap z-order with the previous shape
                prev_shape = all_shapes[idx - 1]
                temp_z = selected_shape.z_order
                selected_shape.z_order = prev_shape.z_order
                prev_shape.z_order = temp_z
        
        # Update property panel if a single shape is selected
        if len(self.canvas.selected_shapes) == 1:
            self.property_panel.update_properties(self.canvas.selected_shapes[0].draw())
            
        self.canvas.notify_observers()
