import tkinter as tk
from tkinter import ttk
from .canvas_view import CanvasView
from .property_panel import PropertyPanel
from .toolbar import Toolbar
from .menu_bar import MenuBar

class MainWindow:
    """
    Main window of the Miridih Paint application.
    Manages the overall UI layout and user interactions.
    """
    
    def __init__(self):
        """Initialize the main window and its components."""
        self._init_window()
        self._create_ui_components()
        self._setup_layout()
    
    def _init_window(self):
        """Initialize the main window properties."""
        self.root = tk.Tk()
        self.root.title("Miridih Paint")
    
    def _create_ui_components(self):
        """Create all UI components."""
        self._create_menu()
        self._create_toolbar()
        self._create_main_frame()
        self._create_canvas()
        self._create_property_panel()
    
    def _setup_layout(self):
        """Set up the layout of UI components."""
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.property_panel.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _create_menu(self):
        """Create the application menu bar."""
        self.menu_bar = MenuBar(self.root)
        self.root.config(menu=self.menu_bar)
    
    def _create_toolbar(self):
        """Create the toolbar with shape selection and mode controls."""
        self.toolbar = Toolbar(
            self.root,
            on_select_mode_changed=self.on_select_mode_changed,
            on_shape_type_changed=self.on_shape_type_changed,
            on_z_order_changed=self.on_z_order_changed
        )
        self.toolbar.pack(fill=tk.X, padx=5, pady=2)
    
    def _create_main_frame(self):
        """Create the main frame container."""
        self.main_frame = tk.Frame(self.root)
    
    def _create_canvas(self):
        """Create the canvas view component."""
        self.canvas_view = CanvasView(self.main_frame)
    
    def _create_property_panel(self):
        """Create the property panel component."""
        self.property_panel = PropertyPanel(self.main_frame)
    
    def on_select_mode_changed(self):
        """Handle select mode toggle."""
        is_select_mode = self.toolbar.get_select_mode()
        if is_select_mode:
            # Disable shape creation temporarily
            self.canvas_view.set_shape_type("select")
        else:
            # Restore previous shape type
            self.canvas_view.set_shape_type(self.toolbar.get_shape_type().lower())
    
    def on_shape_type_changed(self, shape_type):
        """Handle shape type selection change."""
        if not self.toolbar.get_select_mode():
            self.canvas_view.set_shape_type(shape_type.lower())
    
    def on_z_order_changed(self, action):
        """Handle z-order changes."""
        if hasattr(self, 'canvas_view') and hasattr(self.canvas_view, 'canvas_controller'):
            if action == "front":
                self.canvas_view.canvas_controller.bring_to_front()
            elif action == "back":
                self.canvas_view.canvas_controller.send_to_back()
            elif action == "forward":
                self.canvas_view.canvas_controller.bring_forward()
            elif action == "backward":
                self.canvas_view.canvas_controller.send_backward()
    
    def start(self):
        """Start the application main loop."""
        self.root.mainloop() 