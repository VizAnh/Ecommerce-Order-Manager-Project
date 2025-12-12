from tkinter import *
from tkinter import ttk

class NavigationPanel:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.buttons = []
    
    def show(self):
        """Show navigation panel"""
        for widget in self.parent.winfo_children():
            widget.destroy()

        self.parent.grid_columnconfigure(0, weight=1)

        # Application title
        title_frame = Frame(self.parent, bg=self.main_app.COLOUR3)
        title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 20))
        
        Label(title_frame, text="E-commerce Manager", 
              font=(self.main_app.FONT, 16, "bold"), 
              bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack(pady=10)

        # Navigation buttons with better labels and keyboard shortcuts
        nav_options = [
            ("📊 Dashboard", "View analytics and reports", "D", self.main_app.show_dashboard),
            ("🔍 Search & Filter", "Search across all data", "S", self.main_app.show_search),
            ("👥 Manage Customers", "Add, edit, or remove customers", "C", self.main_app.Customer),
            ("📦 Manage Products", "Manage product catalog", "P", self.main_app.Product),
            ("🛒 Manage Orders", "Process and track orders", "O", self.main_app.Order),
            ("📋 Order Quantities", "Manage order items", "Q", self.main_app.Quantity),
        ]

        self.buttons = []
        for i, (text, tooltip, shortcut, command) in enumerate(nav_options):
            btn = Button(self.parent, text=f"{text} (Alt+{shortcut})", 
                        bg=self.main_app.COLOUR2, fg=self.main_app.COLOUR5,
                        font=self.main_app.FONT_STYLE1, 
                        command=command,
                        relief="flat",
                        padx=10,
                        pady=8,
                        anchor="w")
            btn.grid(row=i+1, column=0, padx=10, pady=5, sticky=(E, W))
            self.buttons.append(btn)
            
            # Add tooltip
            self.create_tooltip(btn, tooltip)
            
            # Bind keyboard shortcuts
            self.main_app.root.bind(f"<Alt-{shortcut.lower()}>", lambda e, cmd=command: cmd())
            self.main_app.root.bind(f"<Alt-{shortcut.upper()}>", lambda e, cmd=command: cmd())

        # Spacer
        Frame(self.parent, bg=self.main_app.COLOUR3, height=20).grid(row=len(nav_options)+1, column=0)

        # Add export button to navigation
        export_btn = Button(self.parent, text="📤 Export Data", 
                        bg=self.main_app.COLOUR2, fg=self.main_app.COLOUR5,
                        font=self.main_app.FONT_STYLE1,
                        command=self.main_app.show_export,
                        relief="flat",
                        padx=10,
                        pady=8,
                        anchor="w")
        export_btn.grid(row=len(nav_options)+2, column=0, padx=10, pady=5, sticky=(E, W))
        # self.buttons.append(export_btn)
        
        # Exit button
        exit_btn = Button(self.parent, text="🚪 Exit Application", 
                         bg="#dc3545", fg="white",
                         font=self.main_app.FONT_STYLE1,
                         command=self.main_app.quit_app,  # Changed to use quit_app
                         relief="flat",
                         padx=10,
                         pady=8)
        exit_btn.grid(row=len(nav_options)+3, column=0, padx=10, pady=10, sticky=(E, W))

        # Bind keyboard shortcut
        self.main_app.root.bind("<Alt-E>", lambda e: self.main_app.show_export())
        
        # Bind Escape key to exit - use quit_app
        self.main_app.root.bind("<Escape>", lambda e: self.main_app.quit_app())
        
        # Bind F1 key to help
        self.main_app.root.bind("<F1>", self.show_help)

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+50}+{event.y_root+50}")
            label = Label(tooltip, text=text, background="black", 
                         relief='solid', borderwidth=1, font=(self.main_app.FONT, 10))
            label.pack()
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def show_help(self, event=None):
        """Show keyboard shortcuts help"""
        help_text = """
Keyboard Shortcuts:

Alt+D - Dashboard
Alt+S - Search & Filter  
Alt+C - Customer Management
Alt+P - Product Management
Alt+O - Order Management
Alt+Q - Quantity Management
F1    - This help dialog
Esc   - Exit application

In forms:
Enter - Submit form
Tab   - Navigate between fields
"""
        from tkinter import messagebox
        messagebox.showinfo("Keyboard Shortcuts", help_text.strip())