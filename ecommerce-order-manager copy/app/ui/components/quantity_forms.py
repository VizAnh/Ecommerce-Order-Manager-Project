from tkinter import *
from tkinter import ttk
import threading
from app.models.quantity_model import (
    create_quantity, get_quantity, update_quantity, delete_quantity, get_all_quantities
)
from app.models.order_model import get_all_orders
from app.models.product_model import get_all_products

class QuantityForms:
    def __init__(self, main_app):
        self.main_app = main_app
    
    def show_quantity_management(self):
        """Show quantity management interface"""
        # Clear existing elements
        for widget in self.main_app.F1.winfo_children():
            widget.destroy()
        for widget in self.main_app.F2.winfo_children():
            widget.destroy()

        # Option Selection Panel
        self.F3 = Frame(self.main_app.F1, bg=self.main_app.COLOUR4, padx=15, pady=15)
        self.F3.place(width=self.main_app.ww/4, height=240)

        Label(self.F3, text="Order Quantity Management", font=(self.main_app.FONT, 16, "bold"), 
              bg=self.main_app.COLOUR4, fg=self.main_app.COLOUR5).pack(anchor='w', pady=(0, 10))

        # CRUD Options
        self.combo_quantity = ttk.Combobox(self.F3, font=self.main_app.FONT_STYLE1, state='readonly')
        self.combo_quantity['values'] = [
            '➕ Add New Quantity',
            '🔍 Search Quantity by IDs', 
            '✏️ Edit Existing Quantity',
            '🗑️ Delete Quantity'
        ]
        self.combo_quantity.pack(fill='x', pady=5)
        self.combo_quantity.set('Select an action...')

        self.combo_quantity.bind("<<ComboboxSelected>>", self.QuantityOptions)

        # Help text
        help_label = Label(self.F3, text="💡 You need both Order ID and Product ID",
                          font=(self.main_app.FONT, 9), bg=self.main_app.COLOUR4, fg=self.main_app.COLOUR2)
        help_label.pack(anchor='w', pady=(5, 0))
        
        quantity_help = Label(self.F3, text="🔢 Quantity must be greater than 0",
                          font=(self.main_app.FONT, 9), bg=self.main_app.COLOUR4, fg=self.main_app.COLOUR2)
        quantity_help.pack(anchor='w', pady=(2, 0))

        # Back button
        Button(self.F3, text="← Back to Main Menu", font=self.main_app.FONT_STYLE1, 
               bg=self.main_app.COLOUR2, fg=self.main_app.COLOUR5, 
               command=self.main_app.mainScreen).pack(fill='x', pady=(15, 0))

        # Form Panel
        self.F4 = Frame(self.main_app.F1, bg=self.main_app.COLOUR3)
        self.F4.place(y=240, width=self.main_app.ww/4, height=(self.main_app.wh - 240))
        self.F4.pack_propagate(False)

        # Show empty state initially
        self.show_form_placeholder("Select an action from the dropdown above to manage order quantities.")

        # Table Panel
        self.show_quantity_table()
    
    def show_form_placeholder(self, message):
        """Show placeholder message in form area"""
        for widget in self.F4.winfo_children():
            widget.destroy()
        
        placeholder = Frame(self.F4, bg=self.main_app.COLOUR3)
        placeholder.pack(expand=True, fill=BOTH)
        
        Label(placeholder, text=message, font=self.main_app.FONT_STYLE1,
              bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5, wraplength=300).pack(expand=True)
    
    def QuantityOptions(self, event):
        """Handle quantity option selection"""
        choice = event.widget.get()
        
        # Better way to detect the action
        if 'Add' in choice:
            choice_action = "Add"
        elif 'Search' in choice:
            choice_action = "Search" 
        elif 'Edit' in choice:
            choice_action = "Edit"
        elif 'Delete' in choice:
            choice_action = "Delete"
        else:
            choice_action = "Unknown"
        

        self.main_app.update_status(f"Quantity: {choice_action}")
        
        # Clear previous form
        for widget in self.F4.winfo_children():
            widget.destroy()
        
        # Refresh table
        self.refresh_quantity_table()
        
        # Show appropriate form
        if 'Add' in choice:
            self.form_AddQuantity()
        elif 'Search' in choice:
            self.form_SearchQuantity()
        elif 'Edit' in choice:
            self.form_EditQuantity()
        elif 'Delete' in choice:
            self.form_DeleteQuantity()
        else:
            self.show_form_placeholder(f"No action available for: {choice}")
        
        # Force update to ensure UI refreshes
        self.F4.update_idletasks()
        self.F4.update()
    
    def form_AddQuantity(self):
        """Form for adding new quantity"""
        def validate_quantity(text):
            # Allow empty
            if text == "":
                return True
            # Allow only digits
            return text.isdigit()

        def submit(entries):
            order_id = entries['oid'].get()
            product_id = entries['pid'].get()
            quantity = entries['quantity'].get().strip()
            
            # Validation
            if not order_id:
                self.show_form_error("❌ Order ID is required")
                return
            if not product_id:
                self.show_form_error("❌ Product ID is required")
                return
            if not quantity:
                self.show_form_error("❌ Quantity is required")
                return
            
            try:
                quantity_val = int(quantity)
                if quantity_val <= 0:
                    self.show_form_error("❌ Quantity must be greater than 0")
                    return
            except ValueError:
                self.show_form_error("❌ Quantity must be a whole number")
                return
            
            def execute_create():
                try:
                    msg = create_quantity(order_id, product_id, quantity_val)
                    self.main_app.root.after(0, lambda: self.show_form_success(msg))
                    self.main_app.root.after(0, self.refresh_quantity_table)
                except Exception as e:
                    self.main_app.root.after(0, lambda: self.show_form_error(f"Error: {str(e)}"))
            
            threading.Thread(target=execute_create, daemon=True).start()

        # Get orders and products for dropdowns
        orders = get_all_orders()
        order_ids = [order['OrderID'] for order in orders] if orders else []
        
        products = get_all_products()
        product_ids = [product['ProductID'] for product in products] if products else []
        
        fields = [
            ("Order ID *", "oid", "combobox"),
            ("Product ID *", "pid", "combobox"),
            ("Quantity *", "quantity", "entry")
        ]
        
        help_texts = {
            'oid': "Select the order for this quantity",
            'pid': "Select the product for this quantity",
            'quantity': "Enter the quantity (must be greater than 0)"
        }
        
        entries = self.create_form("Add New Quantity", fields, "Create Quantity", submit, 
                                validate_quantity, help_texts)
        
        # Set combobox values AFTER creating the form
        if 'oid' in entries:
            entries['oid']['values'] = order_ids
        if 'pid' in entries:
            entries['pid']['values'] = product_ids
        
        return entries
    
    def form_SearchQuantity(self):
        """Form for searching quantity by Order ID and Product ID"""
        self.load_form()

        frame = Frame(self.F4, bg=self.main_app.COLOUR3, padx=10, pady=20)
        frame.pack(fill=BOTH, expand=True)

        Label(frame, text="Search Quantity", font=self.main_app.H2_STYLE, 
              bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack(anchor='w', pady=(0, 20))

        # Search inputs
        input_frame = Frame(frame, bg=self.main_app.COLOUR3)
        input_frame.pack(fill='x', pady=10)
        
        # Order ID
        Label(input_frame, text="Order ID:", font=self.main_app.FONT_STYLE1, 
              bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack(anchor='w')
        
        oid_entry = Entry(input_frame, font=self.main_app.FONT_STYLE1, 
                         bg=self.main_app.COLOUR2, fg=self.main_app.COLOUR5)
        oid_entry.pack(fill='x', pady=(5, 0))
        oid_entry.focus_set()

        Label(input_frame, text="Enter Order ID (e.g., O000000001)", 
              font=(self.main_app.FONT, 10), bg=self.main_app.COLOUR3, 
              fg=self.main_app.COLOUR4).pack(anchor='w', pady=(2, 10))

        # Product ID
        Label(input_frame, text="Product ID:", font=self.main_app.FONT_STYLE1, 
              bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack(anchor='w')
        
        pid_entry = Entry(input_frame, font=self.main_app.FONT_STYLE1, 
                         bg=self.main_app.COLOUR2, fg=self.main_app.COLOUR5)
        pid_entry.pack(fill='x', pady=(5, 0))

        Label(input_frame, text="Enter Product ID (e.g., P000000001)", 
              font=(self.main_app.FONT, 10), bg=self.main_app.COLOUR3, 
              fg=self.main_app.COLOUR4).pack(anchor='w', pady=(2, 0))

        # Results label
        results_label = Label(frame, text="", font=(self.main_app.FONT, 10), 
                             bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5)
        results_label.pack(anchor='w', pady=(10, 0))

        def search():
            order_id = oid_entry.get().strip()
            product_id = pid_entry.get().strip()
            
            if not order_id and not product_id:
                results_label.config(text="❌ Please enter at least one ID", fg="red")
                return
            
            # Show loading
            loading_frame = Frame(frame, bg=self.main_app.COLOUR3)
            loading_frame.pack(pady=10)
            Label(loading_frame, text="Searching...", font=self.main_app.FONT_STYLE1, 
                  bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack()
            
            def execute_search():
                try:
                    result = get_quantity(order_id, product_id)
                    self.main_app.root.after(0, loading_frame.destroy)
                    
                    if isinstance(result, list) and len(result) > 0:
                        self.main_app.root.after(0, lambda: self.quantity_table.delete(*self.quantity_table.get_children()))
                        for row in result:
                            self.main_app.root.after(0, lambda r=row: self.quantity_table.insert("", END, values=(
                                r["OrderID"], r["ProductID"], r["Quantity"])))
                        self.main_app.root.after(0, lambda: results_label.config(text=f"✅ Found {len(result)} quantity record(s)", fg="green"))
                    else:
                        self.main_app.root.after(0, lambda: results_label.config(text="❌ No quantity records found", fg="red"))
                        self.main_app.root.after(0, self.refresh_quantity_table)
                except Exception as e:
                    self.main_app.root.after(0, loading_frame.destroy)
                    self.main_app.root.after(0, lambda: results_label.config(text=f"❌ Error: {str(e)}", fg="red"))
            
            threading.Thread(target=execute_search, daemon=True).start()

        # Buttons
        button_frame = Frame(frame, bg=self.main_app.COLOUR3)
        button_frame.pack(fill='x', pady=20)
        
        Button(button_frame, text="🔍 Search", font=self.main_app.FONT_STYLE1,
               bg=self.main_app.COLOUR5, fg="white", command=search).pack(side='left', padx=(0, 10))
        
        Button(button_frame, text="🔄 Reset", font=self.main_app.FONT_STYLE1,
               bg=self.main_app.COLOUR4, fg="white", command=self.refresh_quantity_table).pack(side='left')
        
        # Bind Enter key to search
        oid_entry.bind('<Return>', lambda e: search())
        pid_entry.bind('<Return>', lambda e: search())
    
    def form_EditQuantity(self):
        """Form for editing existing quantity"""
        def validate_quantity(text):
            if not text:
                return True
            try:
                quantity = int(text)
                return quantity > 0
            except ValueError:
                return False

        def submit(entries):
            order_id = entries['oid'].get().strip()
            product_id = entries['pid'].get().strip()
            quantity = entries['quantity'].get().strip()
            
            # Validation
            if not order_id:
                self.show_form_error("❌ Order ID is required")
                return
            if not product_id:
                self.show_form_error("❌ Product ID is required")
                return
            if not quantity:
                self.show_form_error("❌ Quantity is required")
                return
            
            try:
                quantity_val = int(quantity)
                if quantity_val <= 0:
                    self.show_form_error("❌ Quantity must be greater than 0")
                    return
            except ValueError:
                self.show_form_error("❌ Quantity must be a whole number")
                return
            
            def execute_update():
                try:
                    msg = update_quantity(order_id, product_id, quantity_val)
                    self.main_app.root.after(0, lambda: self.show_form_success(msg))
                    self.main_app.root.after(0, self.refresh_quantity_table)
                except Exception as e:
                    self.main_app.root.after(0, lambda: self.show_form_error(f"Error: {str(e)}"))
            
            threading.Thread(target=execute_update, daemon=True).start()

        fields = [
            ("Order ID *", "oid", "entry"),
            ("Product ID *", "pid", "entry"),
            ("New Quantity *", "quantity", "entry")
        ]
        
        help_texts = {
            'oid': "Enter the Order ID you want to edit",
            'pid': "Enter the Product ID you want to edit", 
            'quantity': "Enter the new quantity (must be greater than 0)"
        }
        
        self.create_form("Edit Quantity", fields, "Update Quantity", submit, 
                        validate_quantity, help_texts)
    
    def form_DeleteQuantity(self):
        """Form for deleting quantity"""
        def submit(entries):
            order_id = entries['oid'].get().strip()
            product_id = entries['pid'].get().strip()
            
            if not order_id:
                self.show_form_error("❌ Order ID is required")
                return
            if not product_id:
                self.show_form_error("❌ Product ID is required")
                return
            
            # Confirm deletion
            from tkinter import messagebox
            if not messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete quantity record?\nOrder: {order_id}, Product: {product_id}\nThis action cannot be undone."):
                return
            
            def execute_delete():
                try:
                    msg = delete_quantity(order_id, product_id)
                    self.main_app.root.after(0, lambda: self.show_form_success(msg))
                    self.main_app.root.after(0, self.refresh_quantity_table)
                except Exception as e:
                    self.main_app.root.after(0, lambda: self.show_form_error(f"Error: {str(e)}"))
            
            threading.Thread(target=execute_delete, daemon=True).start()

        fields = [
            ("Order ID *", "oid", "entry"),
            ("Product ID *", "pid", "entry")
        ]
        
        help_texts = {
            'oid': "Enter the Order ID you want to delete",
            'pid': "Enter the Product ID you want to delete"
        }
        
        self.create_form("Delete Quantity", fields, "Delete Quantity", submit, help_texts=help_texts)
    
    def load_form(self):
        """Clear form area"""
        for widget in self.F4.winfo_children():
            widget.destroy()
    
    def create_form(self, title, fields, submit_text, submit_command, validate_func=None, help_texts=None):
        """Create a standardized form"""
        self.load_form()
        
        frame = Frame(self.F4, bg=self.main_app.COLOUR3, padx=15, pady=15)
        frame.pack(fill=BOTH, expand=True)
        
        # Title
        Label(frame, text=title, font=self.main_app.H2_STYLE, 
            bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack(anchor='w', pady=(0, 20))
        
        entries = {}
        
        for i, (label_text, key, field_type) in enumerate(fields):
            field_frame = Frame(frame, bg=self.main_app.COLOUR3)
            field_frame.pack(fill='x', pady=8)
            
            # Label
            Label(field_frame, text=label_text, font=self.main_app.FONT_STYLE1, 
                bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack(anchor='w')
            
            # Help text
            if help_texts and key in help_texts:
                Label(field_frame, text=help_texts[key], font=(self.main_app.FONT, 9), 
                    bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR4).pack(anchor='w')
            
            # Input field
            if field_type == "entry":
                entry = Entry(field_frame, font=self.main_app.FONT_STYLE1, 
                            bg=self.main_app.COLOUR2, fg=self.main_app.COLOUR5)
                entry.pack(fill='x', pady=(5, 0))
                
                # Add validation if provided
                if validate_func:
                    validate_cmd = (field_frame.register(validate_func), '%P')
                    entry.config(validate="key", validatecommand=validate_cmd)
                
                entries[key] = entry
                
            elif field_type == "combobox":
                # Create combobox instead of entry
                combo = ttk.Combobox(field_frame, font=self.main_app.FONT_STYLE1, 
                                    state='readonly')
                combo.pack(fill='x', pady=(5, 0))
                entries[key] = combo
        
        # Message area
        self.msg_label = Label(frame, text="", font=(self.main_app.FONT, 10), 
                            bg=self.main_app.COLOUR3, fg="green")
        self.msg_label.pack(anchor='w', pady=(10, 0))
        
        # Submit button
        Button(frame, text=submit_text, font=self.main_app.FONT_STYLE1,
            bg=self.main_app.COLOUR5, fg="white", 
            command=lambda: submit_command(entries)).pack(fill='x', pady=(20, 0))
        
        return entries
    
    def show_form_error(self, message):
        """Show error message in form"""
        self.msg_label.config(text=message, fg="red")
    
    def show_form_success(self, message):
        """Show success message in form"""
        self.msg_label.config(text=message, fg="green")
    
    def show_quantity_table(self):
        """Show quantity table"""
        self.refresh_quantity_table()
    
    def refresh_quantity_table(self):
        """Refresh quantity table with all data"""
        # Clear table
        for widget in self.main_app.F2.winfo_children():
            widget.destroy()
        
        # Create table frame
        table_frame = Frame(self.main_app.F2, bg=self.main_app.COLOUR4)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Title
        Label(table_frame, text="Quantities", font=self.main_app.H2_STYLE,
              bg=self.main_app.COLOUR4, fg="white").pack(anchor='w', pady=(0, 10))
        
        # Create table
        self.quantity_table = ttk.Treeview(table_frame, columns=("OrderID", "ProductID", "Quantity"), 
                                          show="headings", style="Custom.Treeview")
        
        self.quantity_table.heading("OrderID", text="Order ID")
        self.quantity_table.heading("ProductID", text="Product ID")
        self.quantity_table.heading("Quantity", text="Quantity")
        
        self.quantity_table.column("OrderID", width=150, anchor="w")
        self.quantity_table.column("ProductID", width=300, anchor="w")
        self.quantity_table.column("Quantity", width=300, anchor="w")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.quantity_table.yview)
        self.quantity_table.configure(yscrollcommand=scrollbar.set)
        
        self.quantity_table.pack(side='left', fill=BOTH, expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load data
        def load_data():
            try:
                quantities = get_all_quantities()
                self.main_app.root.after(0, lambda: self.populate_table(quantities))
            except Exception as e:
                self.main_app.root.after(0, lambda: self.show_table_error(f"Error loading quantities: {str(e)}"))
        
        threading.Thread(target=load_data, daemon=True).start()
    
    def populate_table(self, data):
        """Populate table with data"""
        self.quantity_table.delete(*self.quantity_table.get_children())
        
        if not data:
            self.quantity_table.insert("", "end", values=("No quantities found", "Add quantities using the form"))
            return
        
        for row in data:
            self.quantity_table.insert("", "end", values=(row["OrderID"], row["ProductID"], row["Quantity"]))
    
    def show_table_error(self, message):
        """Show error in table"""
        self.quantity_table.delete(*self.quantity_table.get_children())
        self.quantity_table.insert("", "end", values=("Error", message))