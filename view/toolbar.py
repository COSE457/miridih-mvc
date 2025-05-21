import tkinter as tk
from tkinter import ttk

class Toolbar(ttk.Frame):
    """
    Toolbar component for the Miridih Paint application.
    Handles shape selection and mode controls.
    """
    
    def __init__(self, master, on_select_mode_changed, on_shape_type_changed, on_z_order_changed):
        """
        Initialize the toolbar.
        
        Args:
            master: Parent widget
            on_select_mode_changed: Callback for select mode changes
            on_shape_type_changed: Callback for shape type changes
            on_z_order_changed: Callback for z-order changes
        """
        super().__init__(master)
        self.on_select_mode_changed = on_select_mode_changed
        self.on_shape_type_changed = on_shape_type_changed
        self.on_z_order_changed = on_z_order_changed
        
        self._init_variables()
        self._create_widgets()
    
    def _init_variables(self):
        """Initialize toolbar variables."""
        self.select_mode_var = tk.BooleanVar(value=False)
        self.shape_var = tk.StringVar(value="Rectangle")
    
    def _create_widgets(self):
        """Create toolbar widgets."""
        self._create_select_mode_button()
        self._create_shape_selection()
        self._create_z_order_controls()
    
    def _create_select_mode_button(self):
        """Create the select mode toggle button."""
        select_button = ttk.Checkbutton(
            self, 
            text="Select Mode",
            variable=self.select_mode_var,
            command=self.on_select_mode_changed
        )
        select_button.pack(side=tk.LEFT, padx=5)
    
    def _create_shape_selection(self):
        """Create the shape type selection dropdown."""
        ttk.Label(self, text="Shape:").pack(side=tk.LEFT, padx=5)
        shapes = ["Rectangle", "Ellipse", "Line", "Text", "Image"]
        shape_menu = ttk.OptionMenu(
            self, self.shape_var, "Rectangle", *shapes,
            command=self.on_shape_type_changed
        )
        shape_menu.pack(side=tk.LEFT, padx=5)
    
    def _create_z_order_controls(self):
        """Create z-order control buttons."""
        z_order_frame = ttk.Frame(self)
        z_order_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            z_order_frame,
            text="Bring to Front",
            command=lambda: self.on_z_order_changed("front")
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            z_order_frame,
            text="Send to Back",
            command=lambda: self.on_z_order_changed("back")
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            z_order_frame,
            text="Bring Forward",
            command=lambda: self.on_z_order_changed("forward")
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            z_order_frame,
            text="Send Backward",
            command=lambda: self.on_z_order_changed("backward")
        ).pack(side=tk.LEFT, padx=2)
    
    def get_select_mode(self):
        """Get the current select mode state."""
        return self.select_mode_var.get()
    
    def get_shape_type(self):
        """Get the current shape type."""
        return self.shape_var.get() 