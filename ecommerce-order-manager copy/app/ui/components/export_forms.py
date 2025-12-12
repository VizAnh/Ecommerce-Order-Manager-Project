from tkinter import *
from tkinter import ttk
import threading
import os
from app.services.export_service import ExportService

class ExportForms:
    def __init__(self, main_app):
        self.main_app = main_app
        self.export_service = ExportService()
    
    def show_export_interface(self):
        """Show export data interface"""
        # Clear existing elements
        for widget in self.main_app.F1.winfo_children():
            widget.destroy()
        for widget in self.main_app.F2.winfo_children():
            widget.destroy()

        # Option Selection Panel
        self.F3 = Frame(self.main_app.F1, bg=self.main_app.COLOUR4, padx=15, pady=15)
        self.F3.place(width=self.main_app.ww/4, height=300)

        Label(self.F3, text="Data Export", font=(self.main_app.FONT, 16, "bold"), 
            bg=self.main_app.COLOUR4, fg=self.main_app.COLOUR5).pack(anchor='w', pady=(0, 10))

        # Export Options
        Label(self.F3, text="Select data to export:", 
            font=self.main_app.FONT_STYLE1, bg=self.main_app.COLOUR4, 
            fg=self.main_app.COLOUR5).pack(anchor='w', pady=(10, 5))

        # Export buttons
        export_options = [
            ("👥 Export Customers", "Export all customer data", self.export_customers),
            ("📦 Export Products", "Export product catalog", self.export_products),
            ("🛒 Export Orders", "Export order records", self.export_orders),
            ("📋 Export Quantities", "Export order items", self.export_quantities),
            ("📊 Orders with Details", "Orders with customer info and totals", self.export_orders_detailed),
            ("💰 Sales Report", "Sales and revenue by product", self.export_sales_report),
        ]

        for text, tooltip, command in export_options:
            btn = Button(self.F3, text=text, 
                        bg=self.main_app.COLOUR2, fg=self.main_app.COLOUR5,
                        font=(self.main_app.FONT, 12),
                        command=command,
                        relief="flat",
                        padx=10,
                        pady=8,
                        anchor="w")
            btn.pack(fill='x', pady=3)
            self.create_tooltip(btn, tooltip)

        # Help text
        help_label = Label(self.F3, text="💡 Files are saved in 'exports' folder",
                        font=(self.main_app.FONT, 9), bg=self.main_app.COLOUR4, fg=self.main_app.COLOUR2)
        help_label.pack(anchor='w', pady=(15, 0))

        # Back button - MOVE THIS HIGHER and make it more prominent
        back_button = Button(self.F3, text="← Back to Main Menu", font=self.main_app.FONT_STYLE1, 
                bg=self.main_app.COLOUR5, fg="white",  # Changed to make it stand out
                command=self.go_back_to_main,
                relief="raised",
                padx=10,
                pady=10)
        back_button.pack(fill='x', pady=(20, 0))
        
        self.main_app.root.bind("<Escape>", lambda e: self.go_back_to_main())

        # Results Panel
        self.F4 = Frame(self.main_app.F1, bg=self.main_app.COLOUR3)
        self.F4.place(y=300, width=self.main_app.ww/4, height=(self.main_app.wh - 300))
        self.F4.pack_propagate(False)

        # Show export history
        self.show_export_history()

        # Table Panel - Show exported files
        self.show_exported_files_table()

    def go_back_to_main(self):
        """Go back to main menu"""
        self.main_app.mainScreen()
    
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
    
    def show_export_history(self):
        """Show export status and history"""
        for widget in self.F4.winfo_children():
            widget.destroy()
        
        frame = Frame(self.F4, bg=self.main_app.COLOUR3, padx=15, pady=15)
        frame.pack(fill=BOTH, expand=True)
        
        Label(frame, text="Export Status", font=self.main_app.H2_STYLE, 
              bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack(anchor='w', pady=(0, 10))
        
        # Status message
        self.export_status = Label(frame, text="Ready to export data", 
                                  font=(self.main_app.FONT, 10), 
                                  bg=self.main_app.COLOUR3, fg="green")
        self.export_status.pack(anchor='w', pady=(0, 20))
        
        # Refresh button
        Button(frame, text="🔄 Refresh File List", font=self.main_app.FONT_STYLE1,
               bg=self.main_app.COLOUR5, fg="white", 
               command=self.refresh_exported_files).pack(fill='x', pady=(10, 0))
    
    def show_export_status(self, message, is_success=True):
        """Update export status message"""
        color = "green" if is_success else "red"
        self.export_status.config(text=message, fg=color)
    
    def export_customers(self):
        """Export customers data"""
        self.show_export_status("Exporting customers...", True)
        
        def execute_export():
            success, message = self.export_service.export_customers()
            self.main_app.root.after(0, lambda: self.show_export_status(message, success))
            self.main_app.root.after(0, self.refresh_exported_files)
        
        threading.Thread(target=execute_export, daemon=True).start()
    
    def export_products(self):
        """Export products data"""
        self.show_export_status("Exporting products...", True)
        
        def execute_export():
            success, message = self.export_service.export_products()
            self.main_app.root.after(0, lambda: self.show_export_status(message, success))
            self.main_app.root.after(0, self.refresh_exported_files)
        
        threading.Thread(target=execute_export, daemon=True).start()
    
    def export_orders(self):
        """Export orders data"""
        self.show_export_status("Exporting orders...", True)
        
        def execute_export():
            success, message = self.export_service.export_orders()
            self.main_app.root.after(0, lambda: self.show_export_status(message, success))
            self.main_app.root.after(0, self.refresh_exported_files)
        
        threading.Thread(target=execute_export, daemon=True).start()
    
    def export_quantities(self):
        """Export quantities data"""
        self.show_export_status("Exporting quantities...", True)
        
        def execute_export():
            success, message = self.export_service.export_quantities()
            self.main_app.root.after(0, lambda: self.show_export_status(message, success))
            self.main_app.root.after(0, self.refresh_exported_files)
        
        threading.Thread(target=execute_export, daemon=True).start()
    
    def export_orders_detailed(self):
        """Export orders with details"""
        self.show_export_status("Exporting orders with details...", True)
        
        def execute_export():
            success, message = self.export_service.export_orders_with_details()
            self.main_app.root.after(0, lambda: self.show_export_status(message, success))
            self.main_app.root.after(0, self.refresh_exported_files)
        
        threading.Thread(target=execute_export, daemon=True).start()
    
    def export_sales_report(self):
        """Export sales report"""
        self.show_export_status("Exporting sales report...", True)
        
        def execute_export():
            success, message = self.export_service.export_sales_report()
            self.main_app.root.after(0, lambda: self.show_export_status(message, success))
            self.main_app.root.after(0, self.refresh_exported_files)
        
        threading.Thread(target=execute_export, daemon=True).start()
    
    def show_exported_files_table(self):
        """Show table of exported files with back button"""
        # Clear table area first
        for widget in self.main_app.F2.winfo_children():
            widget.destroy()
        
        # Create main container
        main_container = Frame(self.main_app.F2, bg=self.main_app.COLOUR4)
        main_container.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Header frame with title and back button
        header_frame = Frame(main_container, bg=self.main_app.COLOUR4)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Back button in header
        back_btn = Button(header_frame, text="← Back", font=(self.main_app.FONT, 12),
                        bg=self.main_app.COLOUR5, fg="white",
                        command=self.go_back_to_main,
                        relief="raised",
                        padx=15,
                        pady=5)
        back_btn.pack(side='left', padx=(0, 20))
        
        # Title
        title_label = Label(header_frame, text="Exported Files", font=self.main_app.H2_STYLE,
                        bg=self.main_app.COLOUR4, fg="white")
        title_label.pack(side='left')
        
        # Table container
        table_frame = Frame(main_container, bg=self.main_app.COLOUR4)
        table_frame.pack(fill=BOTH, expand=True)
        
        # Create table
        self.files_table = ttk.Treeview(table_frame, columns=("Filename", "Size", "Modified"), 
                                    show="headings", style="Custom.Treeview")
        
        self.files_table.heading("Filename", text="Filename")
        self.files_table.heading("Size", text="Size")
        self.files_table.heading("Modified", text="Last Modified")
        
        self.files_table.column("Filename", width=300, anchor="w")
        self.files_table.column("Size", width=150, anchor="w")
        self.files_table.column("Modified", width=200, anchor="w")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.files_table.yview)
        self.files_table.configure(yscrollcommand=scrollbar.set)
        
        self.files_table.pack(side='left', fill=BOTH, expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load data
        def load_data():
            try:
                files = self.export_service.get_export_files()
                self.main_app.root.after(0, lambda: self.populate_files_table(files))
            except Exception as e:
                self.main_app.root.after(0, lambda: self.show_table_error(f"Error loading files: {str(e)}"))
        
        threading.Thread(target=load_data, daemon=True).start()
    
    def refresh_exported_files(self):
        """Refresh the exported files table"""
        for widget in self.main_app.F2.winfo_children():
            widget.destroy()
        
        # Create table frame
        table_frame = Frame(self.main_app.F2, bg=self.main_app.COLOUR4)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Title
        Label(table_frame, text="Exported Files", font=self.main_app.H2_STYLE,
              bg=self.main_app.COLOUR4, fg="white").pack(anchor='w', pady=(0, 10))
        
        # Create table
        self.files_table = ttk.Treeview(table_frame, columns=("Filename", "Size", "Modified"), 
                                       show="headings", style="Custom.Treeview")
        
        self.files_table.heading("Filename", text="Filename")
        self.files_table.heading("Size", text="Size")
        self.files_table.heading("Modified", text="Last Modified")
        
        self.files_table.column("Filename", width=300, anchor="w")
        self.files_table.column("Size", width=150, anchor="w")
        self.files_table.column("Modified", width=200, anchor="w")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.files_table.yview)
        self.files_table.configure(yscrollcommand=scrollbar.set)
        
        self.files_table.pack(side='left', fill=BOTH, expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load data
        def load_data():
            try:
                files = self.export_service.get_export_files()
                self.main_app.root.after(0, lambda: self.populate_files_table(files))
            except Exception as e:
                self.main_app.root.after(0, lambda: self.show_table_error(f"Error loading files: {str(e)}"))
        
        threading.Thread(target=load_data, daemon=True).start()
    
    def populate_files_table(self, files):
        """Populate table with exported files"""
        self.files_table.delete(*self.files_table.get_children())
        
        if not files:
            self.files_table.insert("", "end", values=("No exported files found", "Export data to see files here"))
            return
        
        for file_info in files:
            size_kb = f"{file_info['size'] / 1024:.1f} KB"
            self.files_table.insert("", "end", values=(
                file_info['name'], 
                size_kb, 
                file_info['modified']
            ))
    
    def show_table_error(self, message):
        """Show error in table"""
        self.files_table.delete(*self.files_table.get_children())
        self.files_table.insert("", "end", values=("Error", message))