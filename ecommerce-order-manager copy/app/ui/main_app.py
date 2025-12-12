from tkinter import *
from tkinter import ttk
import threading
from app.ui.components.constants import ConstMeta
from app.ui.components.navigation import NavigationPanel
from app.ui.components.customer_forms import CustomerForms
from app.ui.components.product_forms import ProductForms
from app.ui.components.order_forms import OrderForms
from app.ui.components.quantity_forms import QuantityForms
from app.ui.components.export_forms import ExportForms
from app.ui.dashboard import Dashboard
from app.ui.search import SearchAndFilter

class eCommerce(metaclass=ConstMeta):
    
    FONT = 'Courier'
    FONT_STYLE1 = (FONT, 14)
    H2_STYLE = (FONT, 18, "bold")
    
    COLOUR1 = "#ffffff"  # White
    COLOUR2 = "#f8f9fa"  # Light gray
    COLOUR3 = "#f7d6ad"  # Beige
    COLOUR4 = "#9c8870"  # Brown
    COLOUR5 = "#002b4a"  # Dark blue
    
    def __init__(self, root: Tk) -> None:
        self.root = root
        self.setup_window()
        self.create_widgets()
        self.setup_styles()
        self.show_loading_screen()
        
        # Initialize form handlers
        self.customer_forms = CustomerForms(self)
        self.product_forms = ProductForms(self)
        self.order_forms = OrderForms(self)
        self.quantity_forms = QuantityForms(self)
        self.export_forms = ExportForms(self)
        
        # Properly handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        
        # Load data after a short delay to show loading screen
        self.root.after(100, self.finish_loading)
    
    def quit_app(self):
        """Properly quit the application"""
        print("Shutting down application...")  # Debug
        self.root.quit()     # Stop the mainloop
        self.root.destroy()  # Destroy all widgets
        # Force exit if needed (uncomment if still having issues)
        # import os
        # os._exit(0)
    
    def setup_window(self):
        """Configure the main window"""
        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()
        
        self.root.title('E-commerce Order Manager')
        self.root.geometry(f"{self.w}x{self.h}+0+0")
        self.root.configure(bg=self.COLOUR4)
        
        # Set window icon (if available)
        try:
            # self.root.iconbitmap('app/ui/assets/icon.ico')  # Uncomment if you have an icon
            pass
        except:
            pass
        
        self.root.update_idletasks()
        self.ww = self.root.winfo_width()
        self.wh = self.root.winfo_height()
    
    def create_widgets(self):
        """Create main application widgets"""
        # Navigation Panel
        self.F1 = Frame(self.root, bg=self.COLOUR3)
        self.F1.place(width=(self.ww/4), height=(self.wh))
        
        # Main Content Panel
        self.F2 = Frame(self.root, bg=self.COLOUR4)
        self.F2.place(x=(self.ww/4), width=(3*self.ww/4), height=(self.wh))
        
        # Status Bar
        self.status_bar = Label(self.root, text="Ready", bg=self.COLOUR5, fg="white", 
                               font=(self.FONT, 10), anchor='w')
        self.status_bar.place(x=0, y=self.wh-25, width=self.ww, height=25)
    
    def setup_styles(self):
        """Configure ttk styles"""
        self.style = ttk.Style()
        
        # Table styling
        self.style.configure(
            "Custom.Treeview",
            background="#e9ecef",
            foreground=self.COLOUR5,
            fieldbackground="#dee2e6",
            rowheight=28,
            font=(self.FONT, 12)
        )

        self.style.configure(
            "Custom.Treeview.Heading",
            background=self.COLOUR5,
            foreground="white",
            font=(self.FONT, 12, "bold"),
            padding=(10, 5)
        )

        self.style.map(
            "Custom.Treeview",
            background=[("selected", "#007bff")],
            foreground=[("selected", "white")]
        )
        
        # Button styling
        self.style.configure(
            "Action.TButton",
            font=self.FONT_STYLE1,
            padding=(10, 5)
        )
    
    def show_loading_screen(self):
        """Show loading screen while initializing"""
        for widget in self.F2.winfo_children():
            widget.destroy()
            
        loading_frame = Frame(self.F2, bg=self.COLOUR4)
        loading_frame.pack(expand=True, fill=BOTH)
        
        Label(loading_frame, text="E-commerce Order Manager", 
              font=(self.FONT, 24, "bold"), bg=self.COLOUR4, fg="white").pack(pady=50)
        
        Label(loading_frame, text="Loading...", 
              font=(self.FONT, 14), bg=self.COLOUR4, fg="white").pack()
        
        # Progress bar
        self.loading_progress = ttk.Progressbar(loading_frame, mode='indeterminate')
        self.loading_progress.pack(pady=20, ipadx=200)
        self.loading_progress.start()
        
        Label(loading_frame, text="Please wait while we load your data...", 
              font=(self.FONT, 10), bg=self.COLOUR4, fg="white").pack()
    
    def finish_loading(self):
        """Finish loading and show main screen"""
        self.loading_progress.stop()
        self.mainScreen()
        self.update_status("Application ready")
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.config(text=f" {message}")
    
    def show_error(self, message, parent=None):
        """Show error message dialog"""
        from tkinter import messagebox
        messagebox.showerror("Error", message, parent=parent or self.root)
    
    def show_info(self, message, parent=None):
        """Show info message dialog"""
        from tkinter import messagebox
        messagebox.showinfo("Information", message, parent=parent or self.root)
    
    def mainScreen(self):
        """Show main navigation screen"""
        # Use the NavigationPanel component
        for widget in self.F1.winfo_children():
            widget.destroy()
        for widget in self.F2.winfo_children():
            widget.destroy()

        # Create navigation panel
        self.nav_panel = NavigationPanel(self.F1, self)
        self.nav_panel.show()
        
        # Show dashboard by default
        self.show_dashboard()
    
    # Navigation methods
    def show_dashboard(self):
        self.update_status("Loading dashboard...")
        for widget in self.F2.winfo_children():
            widget.destroy()
        dashboard = Dashboard(self.F2, self)
        dashboard.show()
        self.update_status("Dashboard loaded")
    
    def show_search(self):
        self.update_status("Loading search...")
        for widget in self.F2.winfo_children():
            widget.destroy()
        search = SearchAndFilter(self.F2, self)
        search.show()
        self.update_status("Search and filter ready")
    
    def show_export(self):
        self.update_status("Data export")
        self.export_forms.show_export_interface()
    
    def Customer(self):
        self.update_status("Customer management")
        self.customer_forms.show_customer_management()
    
    def Product(self):
        self.update_status("Product management")
        self.product_forms.show_product_management()
    
    def Order(self):
        self.update_status("Order management")
        self.order_forms.show_order_management()
    
    def Quantity(self):
        self.update_status("Order quantity management")
        self.quantity_forms.show_quantity_management()