from tkinter import *
from tkinter import ttk
import threading
from app.models.customer_model import (
    create_customer, get_customer, update_customer, delete_customer, get_all_customers
)

class CustomerForms:
    def __init__(self, main_app):
        self.main_app = main_app
    
    def show_customer_management(self):
        """Show customer management interface"""
        # Clear existing elements
        for widget in self.main_app.F1.winfo_children():
            widget.destroy()
        for widget in self.main_app.F2.winfo_children():
            widget.destroy()

        # Option Selection Panel
        self.F3 = Frame(self.main_app.F1, bg=self.main_app.COLOUR4, padx=15, pady=15)
        self.F3.place(width=self.main_app.ww/4, height=200)

        Label(self.F3, text="Customer Management", font=(self.main_app.FONT, 16, "bold"), 
              bg=self.main_app.COLOUR4, fg=self.main_app.COLOUR5).pack(anchor='w', pady=(0, 10))

        # CRUD Options with better labels
        self.combo_customer = ttk.Combobox(self.F3, font=self.main_app.FONT_STYLE1, state='readonly')
        self.combo_customer['values'] = [
            '➕ Add New Customer',
            '🔍 Search Customer by ID', 
            '✏️ Edit Existing Customer',
            '🗑️ Delete Customer'
        ]
        self.combo_customer.pack(fill='x', pady=5)
        self.combo_customer.set('Select an action...')  # Default hint

        self.combo_customer.bind("<<ComboboxSelected>>", self.CustomerOptions)

        # Help text
        help_label = Label(self.F3, text="💡 Customer ID format: C followed by 9 digits (e.g., C000000001)",
                          font=(self.main_app.FONT, 9), bg=self.main_app.COLOUR4, fg=self.main_app.COLOUR2)
        help_label.pack(anchor='w', pady=(10, 0))

        # Back button
        Button(self.F3, text="← Back to Main Menu", font=self.main_app.FONT_STYLE1, 
               bg=self.main_app.COLOUR2, fg=self.main_app.COLOUR5, 
               command=self.main_app.mainScreen).pack(fill='x', pady=(15, 0))

        # Form Panel
        self.F4 = Frame(self.main_app.F1, bg=self.main_app.COLOUR3)
        self.F4.place(y=200, width=self.main_app.ww/4, height=(self.main_app.wh - 200))
        self.F4.pack_propagate(False)

        # Show empty state initially
        self.show_form_placeholder("Select an action from the dropdown above to manage customers.")

        # Table Panel
        self.show_customer_table()
    
    def show_form_placeholder(self, message):
        """Show placeholder message in form area"""
        for widget in self.F4.winfo_children():
            widget.destroy()
        
        placeholder = Frame(self.F4, bg=self.main_app.COLOUR3)
        placeholder.pack(expand=True, fill=BOTH)
        
        Label(placeholder, text=message, font=self.main_app.FONT_STYLE1,
              bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5, wraplength=300).pack(expand=True)
    
    def CustomerOptions(self, event):
        """Handle customer option selection"""
        choice = event.widget.get()
        print(f"DEBUG: Customer option selected: '{choice}'")  # Debug print
        
        # Better way to detect the action - check for keywords instead of splitting
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
            print(f"DEBUG: Unknown choice: {choice}")
        
        print(f"DEBUG: Detected action: {choice_action}")  # Debug print
        self.main_app.update_status(f"Customer: {choice_action}")
        
        # Clear previous form
        for widget in self.F4.winfo_children():
            widget.destroy()
        print(f"DEBUG: F4 cleared, children: {len(self.F4.winfo_children())}")  # Debug print
        
        # Refresh table
        self.refresh_customer_table()
        
        # Show appropriate form - use the actual choice string for matching
        print(f"DEBUG: Calling form method for: {choice_action}")  # Debug print
        
        if 'Add' in choice:
            print("DEBUG: Calling form_AddCustomer")  # Debug print
            self.form_AddCustomer()
        elif 'Search' in choice:
            print("DEBUG: Calling form_SearchCustomer")  # Debug print
            self.form_SearchCustomer()
        elif 'Edit' in choice:
            print("DEBUG: Calling form_EditCustomer")  # Debug print
            self.form_EditCustomer()
        elif 'Delete' in choice:
            print("DEBUG: Calling form_DeleteCustomer")  # Debug print
            self.form_DeleteCustomer()
        else:
            print(f"DEBUG: No form method matched for choice: {choice}")
            self.show_form_placeholder(f"No action available for: {choice}")
        
        print(f"DEBUG: After form call, F4 children: {len(self.F4.winfo_children())}")  # Debug print
        
        # Force update to ensure UI refreshes
        self.F4.update_idletasks()
        self.F4.update()
    
    def form_AddCustomer(self):
        """Form for adding new customer"""
        def validate_customer_id(text):
            # Allow empty (for backspace/delete)
            if text == "":
                return True
            # Check length
            if len(text) > 10:  # C + 9 digits = 10 characters
                return False
            # If starts with C, the rest should be digits
            if text.startswith('C'):
                # After C, only digits allowed
                rest = text[1:]
                return rest == "" or rest.isdigit()
            # If doesn't start with C yet, allow typing
            return True
        
        def submit(entries):
            customer_id = entries['cid'].get().strip()
            customer_name = entries['cname'].get().strip()
            
            # Final validation in submit (more strict)
            if not customer_id:
                self.show_form_error("❌ Customer ID is required")
                return
            if not customer_name:
                self.show_form_error("❌ Customer name is required")
                return
            if not (customer_id.startswith('C') and customer_id[1:].isdigit() and len(customer_id) == 10):
                self.show_form_error("❌ Customer ID must be in format: C + 9 digits (e.g., C000000001)")
                return
            
            def execute_create():
                try:
                    msg = create_customer(customer_id, customer_name)
                    self.main_app.root.after(0, lambda: self.show_form_success(msg))
                    self.main_app.root.after(0, self.refresh_customer_table)
                except Exception as e:
                    self.main_app.root.after(0, lambda: self.show_form_error(f"Error: {str(e)}"))
            
            threading.Thread(target=execute_create, daemon=True).start()

        fields = [
            ("Customer ID *", "cid", "entry"),
            ("Customer Name *", "cname", "entry")
        ]
        
        help_texts = {
            'cid': "Format: C followed by 9 digits (e.g., C000000001)",
            'cname': "Enter the full name of the customer"
        }
        
        self.create_form("Add New Customer", fields, "Create Customer", submit, 
                        validate_customer_id, help_texts)
    
    def form_SearchCustomer(self):
        """Form for searching customer by ID"""
        self.load_form()

        frame = Frame(self.F4, bg=self.main_app.COLOUR3, padx=10, pady=20)
        frame.pack(fill=BOTH, expand=True)

        Label(frame, text="Search Customer", font=self.main_app.H2_STYLE, 
              bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack(anchor='w', pady=(0, 20))

        # Search input
        input_frame = Frame(frame, bg=self.main_app.COLOUR3)
        input_frame.pack(fill='x', pady=10)
        
        Label(input_frame, text="Customer ID:", font=self.main_app.FONT_STYLE1, 
              bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack(anchor='w')
        
        cid_entry = Entry(input_frame, font=self.main_app.FONT_STYLE1, 
                         bg=self.main_app.COLOUR2, fg=self.main_app.COLOUR5)
        cid_entry.pack(fill='x', pady=(5, 0))
        cid_entry.focus_set()

        # Help text
        Label(input_frame, text="Enter Customer ID to search (e.g., C000000001)", 
              font=(self.main_app.FONT, 10), bg=self.main_app.COLOUR3, 
              fg=self.main_app.COLOUR4).pack(anchor='w', pady=(2, 0))

        # Results label
        results_label = Label(frame, text="", font=(self.main_app.FONT, 10), 
                             bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5)
        results_label.pack(anchor='w', pady=(10, 0))

        def search():
            customer_id = cid_entry.get().strip()
            if not customer_id:
                results_label.config(text="❌ Please enter a Customer ID", fg="red")
                return
            
            # Show loading
            loading_frame = Frame(frame, bg=self.main_app.COLOUR3)
            loading_frame.pack(pady=10)
            Label(loading_frame, text="Searching...", font=self.main_app.FONT_STYLE1, 
                  bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack()
            
            def execute_search():
                try:
                    result = get_customer(customer_id)
                    self.main_app.root.after(0, loading_frame.destroy)
                    
                    if isinstance(result, list) and len(result) > 0:
                        self.main_app.root.after(0, lambda: self.customer_table.delete(*self.customer_table.get_children()))
                        for row in result:
                            self.main_app.root.after(0, lambda r=row: self.customer_table.insert("", END, values=(r["CustomerID"], r["CustomerName"])))
                        self.main_app.root.after(0, lambda: results_label.config(text=f"✅ Found {len(result)} customer(s)", fg="green"))
                    else:
                        self.main_app.root.after(0, lambda: results_label.config(text="❌ No customer found with that ID", fg="red"))
                        self.main_app.root.after(0, self.refresh_customer_table)
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
               bg=self.main_app.COLOUR4, fg="white", command=self.refresh_customer_table).pack(side='left')
        
        # Bind Enter key to search
        cid_entry.bind('<Return>', lambda e: search())
    
    def form_EditCustomer(self):
        """Form for editing existing customer"""
        def submit(entries):
            customer_id = entries['cid'].get().strip()
            customer_name = entries['cname'].get().strip()
            
            # Validation
            if not customer_id:
                self.show_form_error("❌ Customer ID is required")
                return
            if not customer_name:
                self.show_form_error("❌ Customer name is required")
                return
            
            def execute_update():
                try:
                    msg = update_customer(customer_id, customer_name)
                    self.main_app.root.after(0, lambda: self.show_form_success(msg))
                    self.main_app.root.after(0, self.refresh_customer_table)
                except Exception as e:
                    self.main_app.root.after(0, lambda: self.show_form_error(f"Error: {str(e)}"))
            
            threading.Thread(target=execute_update, daemon=True).start()

        fields = [
            ("Customer ID *", "cid", "entry"),
            ("New Customer Name *", "cname", "entry")
        ]
        
        help_texts = {
            'cid': "Enter the Customer ID you want to edit",
            'cname': "Enter the new name for this customer"
        }
        
        self.create_form("Edit Customer", fields, "Update Customer", submit, help_texts=help_texts)
    
    def form_DeleteCustomer(self):
        """Form for deleting customer"""
        def submit(entries):
            customer_id = entries['cid'].get().strip()
            
            if not customer_id:
                self.show_form_error("❌ Customer ID is required")
                return
            
            # Confirm deletion
            from tkinter import messagebox
            if not messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete customer {customer_id}?\nThis action cannot be undone."):
                return
            
            def execute_delete():
                try:
                    msg = delete_customer(customer_id)
                    self.main_app.root.after(0, lambda: self.show_form_success(msg))
                    self.main_app.root.after(0, self.refresh_customer_table)
                except Exception as e:
                    self.main_app.root.after(0, lambda: self.show_form_error(f"Error: {str(e)}"))
            
            threading.Thread(target=execute_delete, daemon=True).start()

        fields = [
            ("Customer ID *", "cid", "entry")
        ]
        
        help_texts = {
            'cid': "Enter the Customer ID you want to delete"
        }
        
        self.create_form("Delete Customer", fields, "Delete Customer", submit, help_texts=help_texts)
    
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
    
    def show_customer_table(self):
        """Show customer table"""
        self.refresh_customer_table()
    
    def refresh_customer_table(self):
        """Refresh customer table with all data"""
        # Clear table
        for widget in self.main_app.F2.winfo_children():
            widget.destroy()
        
        # Create table frame
        table_frame = Frame(self.main_app.F2, bg=self.main_app.COLOUR4)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Title
        Label(table_frame, text="Customers", font=self.main_app.H2_STYLE,
              bg=self.main_app.COLOUR4, fg="white").pack(anchor='w', pady=(0, 10))
        
        # Create table
        self.customer_table = ttk.Treeview(table_frame, columns=("CustomerID", "CustomerName"), 
                                          show="headings", style="Custom.Treeview")
        
        self.customer_table.heading("CustomerID", text="Customer ID")
        self.customer_table.heading("CustomerName", text="Customer Name")
        
        self.customer_table.column("CustomerID", width=150, anchor="w")
        self.customer_table.column("CustomerName", width=300, anchor="w")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.customer_table.yview)
        self.customer_table.configure(yscrollcommand=scrollbar.set)
        
        self.customer_table.pack(side='left', fill=BOTH, expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load data
        def load_data():
            try:
                customers = get_all_customers()
                self.main_app.root.after(0, lambda: self.populate_table(customers))
            except Exception as e:
                self.main_app.root.after(0, lambda: self.show_table_error(f"Error loading customers: {str(e)}"))
        
        threading.Thread(target=load_data, daemon=True).start()
    
    def populate_table(self, data):
        """Populate table with data"""
        self.customer_table.delete(*self.customer_table.get_children())
        
        if not data:
            self.customer_table.insert("", "end", values=("No customers found", "Add customers using the form"))
            return
        
        for row in data:
            self.customer_table.insert("", "end", values=(row["CustomerID"], row["CustomerName"]))
    
    def show_table_error(self, message):
        """Show error in table"""
        self.customer_table.delete(*self.customer_table.get_children())
        self.customer_table.insert("", "end", values=("Error", message))