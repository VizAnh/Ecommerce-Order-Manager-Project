from tkinter import *
from tkinter import ttk
import threading
from app.models.order_model import (
    create_order, get_order, update_order, delete_order, get_all_orders
)
from app.models.customer_model import get_all_customers

class OrderForms:
    def __init__(self, main_app):
        self.main_app = main_app
    
    def show_order_management(self):
        """Show order management interface"""
        # Clear existing elements
        for widget in self.main_app.F1.winfo_children():
            widget.destroy()
        for widget in self.main_app.F2.winfo_children():
            widget.destroy()

        # Option Selection Panel
        self.F3 = Frame(self.main_app.F1, bg=self.main_app.COLOUR4, padx=15, pady=15)
        self.F3.place(width=self.main_app.ww/4, height=240)

        Label(self.F3, text="Order Management", font=(self.main_app.FONT, 16, "bold"), 
              bg=self.main_app.COLOUR4, fg=self.main_app.COLOUR5).pack(anchor='w', pady=(0, 10))

        # CRUD Options
        self.combo_order = ttk.Combobox(self.F3, font=self.main_app.FONT_STYLE1, state='readonly')
        self.combo_order['values'] = [
            '➕ Add New Order',
            '🔍 Search Order by ID', 
            '✏️ Edit Existing Order',
            '🗑️ Delete Order'
        ]
        self.combo_order.pack(fill='x', pady=5)
        self.combo_order.set('Select an action...')

        self.combo_order.bind("<<ComboboxSelected>>", self.OrderOptions)

        # Help text
        help_label = Label(self.F3, text="💡 Order ID format: O followed by 9 digits (e.g., O000000001)",
                          font=(self.main_app.FONT, 9), bg=self.main_app.COLOUR4, fg=self.main_app.COLOUR2)
        help_label.pack(anchor='w', pady=(5, 0))
        
        status_help = Label(self.F3, text="📊 Status: Pending, Shipped, Delivered, or Cancelled",
                          font=(self.main_app.FONT, 9), bg=self.main_app.COLOUR4, fg=self.main_app.COLOUR2)
        status_help.pack(anchor='w', pady=(2, 0))
        
        date_help = Label(self.F3, text="📅 Date format: YYYY-MM-DD (e.g., 2024-01-15)",
                          font=(self.main_app.FONT, 9), bg=self.main_app.COLOUR4, fg=self.main_app.COLOUR2)
        date_help.pack(anchor='w', pady=(2, 0))

        # Back button
        Button(self.F3, text="← Back to Main Menu", font=self.main_app.FONT_STYLE1, 
               bg=self.main_app.COLOUR2, fg=self.main_app.COLOUR5, 
               command=self.main_app.mainScreen).pack(fill='x', pady=(15, 0))

        # Form Panel
        self.F4 = Frame(self.main_app.F1, bg=self.main_app.COLOUR3)
        self.F4.place(y=240, width=self.main_app.ww/4, height=(self.main_app.wh - 240))
        self.F4.pack_propagate(False)

        # Show empty state initially
        self.show_form_placeholder("Select an action from the dropdown above to manage orders.")

        # Table Panel
        self.show_order_table()
    
    def show_form_placeholder(self, message):
        """Show placeholder message in form area"""
        for widget in self.F4.winfo_children():
            widget.destroy()
        
        placeholder = Frame(self.F4, bg=self.main_app.COLOUR3)
        placeholder.pack(expand=True, fill=BOTH)
        
        Label(placeholder, text=message, font=self.main_app.FONT_STYLE1,
              bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5, wraplength=300).pack(expand=True)
    
    def OrderOptions(self, event):
        """Handle order option selection"""
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
        
        self.main_app.update_status(f"Order: {choice_action}")
        
        # Clear previous form
        for widget in self.F4.winfo_children():
            widget.destroy()
        
        # Refresh table
        self.refresh_order_table()
        
        # Show appropriate form
        if 'Add' in choice:
            self.form_AddOrder()
        elif 'Search' in choice:
            self.form_SearchOrder()
        elif 'Edit' in choice:
            self.form_EditOrder()
        elif 'Delete' in choice:
            self.form_DeleteOrder()
        else:
            self.show_form_placeholder(f"No action available for: {choice}")
        
        # Force update to ensure UI refreshes
        self.F4.update_idletasks()
        self.F4.update()
    
    def form_AddOrder(self):
        """Form for adding new order"""
        def validate_order_id(text):
            # Allow empty (for backspace/delete)
            if text == "":
                return True
            # Check length
            if len(text) > 10:  # O + 9 digits = 10 characters
                return False
            # If starts with O, the rest should be digits
            if text.startswith('O'):
                # After O, only digits allowed
                rest = text[1:]
                return rest == "" or rest.isdigit()
            # If doesn't start with O yet, allow typing
            return True

        def submit(entries):
            order_id = entries['oid'].get().strip()
            customer_id = entries['cid'].get()
            order_date = entries['odate'].get().strip()
            order_status = entries['ostatus'].get()
            
            # Validation
            if not order_id:
                self.show_form_error("❌ Order ID is required")
                return
            if not customer_id:
                self.show_form_error("❌ Customer ID is required")
                return
            if not order_date:
                self.show_form_error("❌ Order date is required")
                return
            if not order_status:
                self.show_form_error("❌ Order status is required")
                return
            if not (order_id.startswith('O') and order_id[1:].isdigit() and len(order_id) == 10):
                self.show_form_error("❌ Order ID must be in format: O + 9 digits (e.g., O000000001)")
                return
            
            # Final date validation
            if order_date.count('-') != 2:
                self.show_form_error("❌ Date must be in format: YYYY-MM-DD")
                return
            try:
                year, month, day = map(int, order_date.split('-'))
                # Basic date validation
                if month < 1 or month > 12 or day < 1 or day > 31:
                    self.show_form_error("❌ Invalid date")
                    return
            except ValueError:
                self.show_form_error("❌ Invalid date format")
                return
            
            def execute_create():
                try:
                    msg = create_order(order_id, customer_id, order_date, order_status)
                    self.main_app.root.after(0, lambda: self.show_form_success(msg))
                    self.main_app.root.after(0, self.refresh_order_table)
                except Exception as e:
                    self.main_app.root.after(0, lambda: self.show_form_error(f"Error: {str(e)}"))
            
            threading.Thread(target=execute_create, daemon=True).start()

        # Get customers for dropdown
        customers = get_all_customers()
        customer_ids = [customer['CustomerID'] for customer in customers] if customers else []
        
        fields = [
            ("Order ID *", "oid", "entry"),
            ("Customer ID *", "cid", "combobox"),
            ("Order Date *", "odate", "entry"),
            ("Order Status *", "ostatus", "combobox")
        ]
        
        help_texts = {
            'oid': "Format: O followed by 9 digits (e.g., O000000001)",
            'cid': "Select the customer who placed this order",
            'odate': "Format: YYYY-MM-DD (e.g., 2024-01-15)",
            'ostatus': "Select the current order status"
        }
        
        entries = self.create_form("Add New Order", fields, "Create Order", submit, 
                                validate_order_id, help_texts)
        
        # Set combobox values AFTER creating the form
        if 'cid' in entries:
            entries['cid']['values'] = customer_ids
        if 'ostatus' in entries:
            entries['ostatus']['values'] = ['Pending', 'Shipped', 'Delivered', 'Cancelled']
        
        return entries
    
    def form_SearchOrder(self):
        """Form for searching order by ID"""
        self.load_form()

        frame = Frame(self.F4, bg=self.main_app.COLOUR3, padx=10, pady=20)
        frame.pack(fill=BOTH, expand=True)

        Label(frame, text="Search Order", font=self.main_app.H2_STYLE, 
              bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack(anchor='w', pady=(0, 20))

        # Search input
        input_frame = Frame(frame, bg=self.main_app.COLOUR3)
        input_frame.pack(fill='x', pady=10)
        
        Label(input_frame, text="Order ID:", font=self.main_app.FONT_STYLE1, 
              bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack(anchor='w')
        
        oid_entry = Entry(input_frame, font=self.main_app.FONT_STYLE1, 
                         bg=self.main_app.COLOUR2, fg=self.main_app.COLOUR5)
        oid_entry.pack(fill='x', pady=(5, 0))
        oid_entry.focus_set()

        # Help text
        Label(input_frame, text="Enter Order ID to search (e.g., O000000001)", 
              font=(self.main_app.FONT, 10), bg=self.main_app.COLOUR3, 
              fg=self.main_app.COLOUR4).pack(anchor='w', pady=(2, 0))

        # Results label
        results_label = Label(frame, text="", font=(self.main_app.FONT, 10), 
                             bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5)
        results_label.pack(anchor='w', pady=(10, 0))

        def search():
            order_id = oid_entry.get().strip()
            if not order_id:
                results_label.config(text="❌ Please enter an Order ID", fg="red")
                return
            
            # Show loading
            loading_frame = Frame(frame, bg=self.main_app.COLOUR3)
            loading_frame.pack(pady=10)
            Label(loading_frame, text="Searching...", font=self.main_app.FONT_STYLE1, 
                  bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack()
            
            def execute_search():
                try:
                    result = get_order(order_id)
                    self.main_app.root.after(0, loading_frame.destroy)
                    
                    if isinstance(result, list) and len(result) > 0:
                        self.main_app.root.after(0, lambda: self.order_table.delete(*self.order_table.get_children()))
                        for row in result:
                            self.main_app.root.after(0, lambda r=row: self.order_table.insert("", END, values=(
                                r["OrderID"], r["CustomerID"], r["OrderDate"], r["OrderStatus"])))
                        self.main_app.root.after(0, lambda: results_label.config(text=f"✅ Found {len(result)} order(s)", fg="green"))
                    else:
                        self.main_app.root.after(0, lambda: results_label.config(text="❌ No order found with that ID", fg="red"))
                        self.main_app.root.after(0, self.refresh_order_table)
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
               bg=self.main_app.COLOUR4, fg="white", command=self.refresh_order_table).pack(side='left')
        
        # Bind Enter key to search
        oid_entry.bind('<Return>', lambda e: search())
    
    def form_EditOrder(self):
        """Form for editing existing order"""
        def validate_date(text):
            if not text:
                return True
            if len(text) != 10:
                return False
            parts = text.split('-')
            if len(parts) != 3:
                return False
            return all(part.isdigit() for part in parts)

        def submit(entries):
            order_id = entries['oid'].get().strip()
            customer_id = entries['cid'].get().strip()
            order_date = entries['date'].get().strip()
            order_status = entries['status'].get()
            
            # Validation
            if not order_id:
                self.show_form_error("❌ Order ID is required")
                return
            if not customer_id:
                self.show_form_error("❌ Customer ID is required")
                return
            if not order_date:
                self.show_form_error("❌ Order date is required")
                return
            if not order_status:
                self.show_form_error("❌ Order status is required")
                return
            if not validate_date(order_date):
                self.show_form_error("❌ Date must be in format: YYYY-MM-DD")
                return
            
            def execute_update():
                try:
                    msg = update_order(order_id, customer_id, order_date, order_status)
                    self.main_app.root.after(0, lambda: self.show_form_success(msg))
                    self.main_app.root.after(0, self.refresh_order_table)
                except Exception as e:
                    self.main_app.root.after(0, lambda: self.show_form_error(f"Error: {str(e)}"))
            
            threading.Thread(target=execute_update, daemon=True).start()

        # Get customers for dropdown
        customers = get_all_customers()
        customer_ids = [customer['CustomerID'] for customer in customers] if customers else []
        
        fields = [
            ("Order ID *", "oid", "entry"),
            ("New Customer ID *", "cid", "combobox"),
            ("New Date *", "date", "entry"),
            ("New Status *", "status", "combobox")
        ]
        
        help_texts = {
            'oid': "Enter the Order ID you want to edit",
            'cid': "Select the new customer for this order",
            'date': "Format: YYYY-MM-DD (e.g., 2024-01-15)",
            'status': "Select the new order status"
        }
        
        entries = self.create_form("Edit Order", fields, "Update Order", submit, help_texts=help_texts)
        
        # Set combobox values
        entries['cid']['values'] = customer_ids
        entries['status']['values'] = ['Pending', 'Shipped', 'Delivered', 'Cancelled']
        
        return entries
    
    def form_DeleteOrder(self):
        """Form for deleting order"""
        def submit(entries):
            order_id = entries['oid'].get().strip()
            
            if not order_id:
                self.show_form_error("❌ Order ID is required")
                return
            
            # Confirm deletion
            from tkinter import messagebox
            if not messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete order {order_id}?\nThis will also delete all associated quantities!\nThis action cannot be undone."):
                return
            
            def execute_delete():
                try:
                    msg = delete_order(order_id)
                    self.main_app.root.after(0, lambda: self.show_form_success(msg))
                    self.main_app.root.after(0, self.refresh_order_table)
                except Exception as e:
                    self.main_app.root.after(0, lambda: self.show_form_error(f"Error: {str(e)}"))
            
            threading.Thread(target=execute_delete, daemon=True).start()

        fields = [
            ("Order ID *", "oid", "entry")
        ]
        
        help_texts = {
            'oid': "Enter the Order ID you want to delete"
        }
        
        self.create_form("Delete Order", fields, "Delete Order", submit, help_texts=help_texts)
    
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
    
    def show_order_table(self):
        """Show order table"""
        self.refresh_order_table()
    
    def refresh_order_table(self):
        """Refresh order table with all data"""
        # Clear table
        for widget in self.main_app.F2.winfo_children():
            widget.destroy()
        
        # Create table frame
        table_frame = Frame(self.main_app.F2, bg=self.main_app.COLOUR4)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Title
        Label(table_frame, text="Orders", font=self.main_app.H2_STYLE,
              bg=self.main_app.COLOUR4, fg="white").pack(anchor='w', pady=(0, 10))
        
        # Create table
        self.order_table = ttk.Treeview(table_frame, columns=("OrderID", "CustomerID", "OrderDate", "OrderStatus"), 
                                          show="headings", style="Custom.Treeview")
        
        self.order_table.heading("OrderID", text="Order ID")
        self.order_table.heading("CustomerID", text="Customer ID")
        self.order_table.heading("OrderDate", text="Order Date")
        self.order_table.heading("OrderStatus", text="Status")
        
        self.order_table.column("OrderID", width=150, anchor="w")
        self.order_table.column("CustomerID", width=300, anchor="w")
        self.order_table.column("OrderDate", width=100, anchor="w")
        self.order_table.column("OrderStatus", width=100, anchor="w")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.order_table.yview)
        self.order_table.configure(yscrollcommand=scrollbar.set)
        
        self.order_table.pack(side='left', fill=BOTH, expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load data
        def load_data():
            try:
                orders = get_all_orders()
                self.main_app.root.after(0, lambda: self.populate_table(orders))
            except Exception as e:
                self.main_app.root.after(0, lambda: self.show_table_error(f"Error loading orders: {str(e)}"))
        
        threading.Thread(target=load_data, daemon=True).start()
    
    def populate_table(self, data):
        """Populate table with data"""
        self.order_table.delete(*self.order_table.get_children())
        
        if not data:
            self.order_table.insert("", "end", values=("No orders found", "Add orders using the form"))
            return
        
        for row in data:
            self.order_table.insert("", "end", values=(row["OrderID"], row["CustomerID"], row["OrderDate"], row["OrderStatus"]))
    
    def show_table_error(self, message):
        """Show error in table"""
        self.order_table.delete(*self.order_table.get_children())
        self.order_table.insert("", "end", values=("Error", message))