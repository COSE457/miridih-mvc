import tkinter as tk
from tkinter import PhotoImage, filedialog, simpledialog
from typing import Callable, Optional, Tuple, List
import os
from model.shape_composite import ShapeComponent, ShapeGroup

class CanvasView(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, bg='white')
        self.bind('<Button-1>', self.on_click)
        self.bind('<B1-Motion>', self.on_drag)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.bind('<Control-Button-1>', self.on_multi_select)
        
        self.start_x = None
        self.start_y = None
        self.current_shape = None
        self.current_shape_type = "rectangle"
        self.multi_select_mode = False
        self.dragging_shape = False
        self.drag_start_x = None
        self.drag_start_y = None
        self.shape_drag_callback = None
        
        self.shape_selected_callback = None
        self.shape_created_callback = None
        self.images = {}  # Store PhotoImage objects
        self.selected_group = ShapeGroup()  # Track selected shapes as a group
    
    def prompt_for_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            try:
                # Store the PhotoImage in self.images
                self.images[file_path] = PhotoImage(file=file_path)
                return file_path
            except Exception as e:
                print(f"Error loading image {file_path}: {e}")
                return None
        return None
    
    def _draw_shadow(self, props, shape_type='rectangle'):
        
        shadow_color = 'gray'
        shadow_steps = 0
        
        for i in range(shadow_steps):
            alpha = 0.3 - (i * 0.1)  # Decreasing opacity
            if shape_type == 'ellipse':
                self.create_oval(
                    props['x'] + i,
                    props['y'] + i,
                    props['x'] + props['width'] + i,
                    props['y'] + props['height'] + i,
                    fill=shadow_color,
                    stipple='gray50',
                    tags=('shadow',)
                )
            else: 
                self.create_rectangle(
                    props['x'] + i,
                    props['y'] + i,
                    props['x'] + props['width'] + i,
                    props['y'] + props['height'] + i,
                    fill=shadow_color,
                    stipple='gray50',
                    tags=('shadow',)
                )
    
    def _draw_image(self, props):
        image_path = props['image_path']
        if image_path and os.path.exists(image_path):
            if image_path not in self.images:
                try:
                    self.images[image_path] = PhotoImage(file=image_path)
                except Exception as e:
                    print(f"Error loading image {image_path}: {e}")
                    return
            
            if props['has_shadow']:
                self._draw_shadow(props, 'image')
            
            try:
                self.create_image(
                    props['x'], props['y'],
                    image=self.images[image_path],
                    anchor='nw'
                )
            except Exception as e:
                print(f"Error drawing image {image_path}: {e}")
            
            if props['has_frame']:
                self.create_rectangle(
                    props['x'], props['y'],
                    props['x'] + props['width'],
                    props['y'] + props['height'],
                    outline='black',
                    width=2
                )
        
    def set_shape_type(self, shape_type: str):
        self.current_shape_type = shape_type
        if shape_type == "text":
            self.master.focus_set()
        elif shape_type == "image":
            self.prompt_for_image()
    
    def prompt_for_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.gif *.bmp")]
        )
        if file_path:
            if file_path not in self.images:
                try:
                    self.images[file_path] = PhotoImage(file=file_path)
                    return file_path
                except:
                    return None
    
    def prompt_for_text(self):
        return simpledialog.askstring("Input", "Enter text:")

    def on_click(self, event):
        # In select mode, only handle selection and dragging
        if self.current_shape_type == "select":
            if self.shape_selected_callback:
                result = self.shape_selected_callback(event.x, event.y, check_only=True)
                if result and result.get('is_selected', False):
                    # If clicking on a selected shape, start dragging
                    self.dragging_shape = True
                    self.drag_start_x = event.x
                    self.drag_start_y = event.y
                else:
                    # Just select the shape
                    if not self.multi_select_mode:
                        self.selected_group.deselect()  # Clear previous selection
                    self.shape_selected_callback(event.x, event.y)
            return

        # For other modes, check if we're clicking on a selected shape first
        if self.shape_selected_callback:
            result = self.shape_selected_callback(event.x, event.y, check_only=True)
            if result and result.get('is_selected', False):
                self.dragging_shape = True
                self.drag_start_x = event.x
                self.drag_start_y = event.y
                return

        # Create new shapes only if not in select mode and not clicking on existing shapes
        if self.current_shape_type == "text":
            user_text = self.prompt_for_text()
            if user_text and self.shape_created_callback:
                self.shape_created_callback(
                    event.x, event.y, 100, 30, 'text',
                    {'text': user_text}
                )
        elif self.current_shape_type == "image":
            file_path = self.prompt_for_image()
            if file_path and self.shape_created_callback:
                self.shape_created_callback(
                    event.x, event.y, 200, 200, 'image',
                    {'image_path': file_path}
                )
        else:
            self.start_x = event.x
            self.start_y = event.y

    def on_multi_select(self, event):
        self.multi_select_mode = True
        if self.shape_selected_callback:
            self.shape_selected_callback(event.x, event.y, multi_select=True)
    
    def on_drag(self, event):
        if self.dragging_shape:
            # Calculate the delta movement
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            
            # Update the drag start position for the next movement
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            
            # Move all selected shapes
            self.selected_group.move(dx, dy)
            
            # Call the callback to update the view
            if self.shape_drag_callback:
                self.shape_drag_callback(dx, dy)
        elif self.start_x is not None and self.start_y is not None and self.current_shape_type != "select":
            self.delete("temp_shape")
            if self.current_shape_type == "line":
                self.create_line(
                    self.start_x, self.start_y, event.x, event.y,
                    fill='black', tags=("temp_shape",)
                )
            elif self.current_shape_type == "rectangle":
                self.create_rectangle(
                    self.start_x, self.start_y, event.x, event.y,
                    outline='black', tags=("temp_shape",)
                )
            elif self.current_shape_type == "ellipse":
                self.create_oval(
                    self.start_x, self.start_y, event.x, event.y,
                    outline='black', tags=("temp_shape",)
                )
    
    def on_release(self, event):
        if self.dragging_shape:
            self.dragging_shape = False
            self.drag_start_x = None
            self.drag_start_y = None
        elif self.current_shape_type not in ["text", "image"] and self.start_x is not None and self.start_y is not None:
            if self.shape_created_callback:
                x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
                x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)
                
                if self.current_shape_type == "line":
                    self.shape_created_callback(
                        self.start_x, self.start_y,
                        event.x - self.start_x,
                        event.y - self.start_y,
                        shape_type=self.current_shape_type
                    )
                else:
                    self.shape_created_callback(
                        x1, y1, x2 - x1, y2 - y1,
                        shape_type=self.current_shape_type
                    )
            self.delete("temp_shape")
        self.start_x = None
        self.start_y = None
        self.multi_select_mode = False
    
    def draw_shapes(self, shapes):
        self.delete("all")
        for shape in shapes:
            props = shape.draw()
            outline = 'blue' if props['selected'] else props.get('outline', 'black')
            
            if props['type'] == 'rectangle':
                self._draw_rectangle(props, outline)
            elif props['type'] == 'ellipse':
                self._draw_ellipse(props, outline)
            elif props['type'] == 'line':
                self._draw_line(props, outline)
            elif props['type'] == 'text':
                self._draw_text(props)
            elif props['type'] == 'image':
                self._draw_image(props)
    
    def _draw_rectangle(self, props, outline):
        if props['has_shadow']:
            self._draw_shadow(props, 'rectangle')
        
        self.create_rectangle(
            props['x'], props['y'],
            props['x'] + props['width'],
            props['y'] + props['height'],
            outline=outline,
            fill=props.get('fill', ''),
            width=2 if props['has_frame'] else 1
        )
        
        if props['text'] and props['text'] != "Multiple":
            self._draw_shape_text(props)
    
    def _draw_ellipse(self, props, outline):
        if props['has_shadow']:
            self._draw_shadow(props, 'ellipse')
        
        self.create_oval(
            props['x'], props['y'],
            props['x'] + props['width'],
            props['y'] + props['height'],
            outline=outline,
            fill=props.get('fill', ''),
            width=2 if props['has_frame'] else 1
        )
        
        if props['text'] and props['text'] != "Multiple":
            self._draw_shape_text(props)
    
    def _draw_line(self, props, outline):
        self.create_line(
            props['x'], props['y'],
            props['x'] + props.get('x2', 0),
            props['y'] + props.get('y2', 0),
            fill=outline,
            width=props.get('width', 1)
        )
    
    def _draw_text(self, props):
        self.create_text(
            props['x'], props['y'],
            text=props['text'],
            font=(props.get('font', 'Arial'), props.get('font_size', 12)),
            fill=props.get('text_color', 'black'),
            anchor='nw'
        )
    
    def _draw_image(self, props):
        if props['image_path'] and os.path.exists(props['image_path']):
            if props['image_path'] not in self.images:
                self.images[props['image_path']] = PhotoImage(file=props['image_path'])
            
            if props['has_shadow']:
                self._draw_shadow(props, 'image')
            
            self.create_image(
                props['x'], props['y'],
                image=self.images[props['image_path']],
                anchor='nw'
            )
            
            if props['has_frame']:
                self.create_rectangle(
                    props['x'], props['y'],
                    props['x'] + props['width'],
                    props['y'] + props['height'],
                    outline='black',
                    width=2
                )
    
    def _draw_shape_text(self, props):
        self.create_text(
            props['x'] + props['width']/2,
            props['y'] + props['height']/2,
            text=props['text']
        )
    
    def set_shape_selected_callback(self, callback: Callable):
        self.shape_selected_callback = callback
    
    def set_shape_created_callback(self, callback: Callable):
        self.shape_created_callback = callback
        
    def set_shape_drag_callback(self, callback: Callable):
        self.shape_drag_callback = callback
