import tkinter as tk

class MenuBar(tk.Menu):
    """
    Menu bar component for the Miridih Paint application.
    Handles file and edit operations.
    """
    
    def __init__(self, master):
        """
        Initialize the menu bar.
        
        Args:
            master: Parent widget
        """
        super().__init__(master)
        self._create_file_menu()
        self._create_edit_menu()
    
    def _create_file_menu(self):
        """Create the file menu with its commands."""
        file_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Exit", command=self.master.quit)
    
    def _create_edit_menu(self):
        """Create the edit menu with its commands."""
        edit_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Delete") 