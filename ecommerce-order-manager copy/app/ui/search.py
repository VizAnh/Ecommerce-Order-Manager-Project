import tkinter as tk
from tkinter import ttk
from app.services.dashboard_service import SearchService

class SearchAndFilter:
    def __init__(self, parent_frame, main_app):
        self.parent = parent_frame
        self.main_app = main_app
        self.service = SearchService()
        
    def show(self):
        # Clear existing widgets
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Create search and filter interface
        self.create_global_search()
        self.create_filters()
        self.create_results_section()
        
    def create_global_search(self):
        search_frame = tk.Frame(self.parent, bg=self.main_app.COLOUR3, pady=10)
        search_frame.pack(fill='x', padx=20)
        
        tk.Label(search_frame, text="Global Search", font=self.main_app.H2_STYLE,
                bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack(anchor='w')
        
        search_container = tk.Frame(search_frame, bg=self.main_app.COLOUR3)
        search_container.pack(fill='x', pady=5)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_container, textvariable=self.search_var, 
                               font=self.main_app.FONT_STYLE1, width=50)
        search_entry.pack(side='left', padx=(0, 10))
        
        search_btn = tk.Button(search_container, text="Search", 
                              font=self.main_app.FONT_STYLE1,
                              command=self.perform_global_search)
        search_btn.pack(side='left')
        
        # Bind Enter key to search
        search_entry.bind('<Return>', lambda e: self.perform_global_search())
    
    def create_filters(self):
        filter_frame = tk.Frame(self.parent, bg=self.main_app.COLOUR3, pady=10)
        filter_frame.pack(fill='x', padx=20)
        
        tk.Label(filter_frame, text="Filter Orders", font=self.main_app.H2_STYLE,
                bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack(anchor='w')
        
        # Filter controls
        controls_frame = tk.Frame(filter_frame, bg=self.main_app.COLOUR3)
        controls_frame.pack(fill='x', pady=5)
        
        # Status filter
        tk.Label(controls_frame, text="Status:", font=self.main_app.FONT_STYLE1,
                bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).grid(row=0, column=0, sticky='w')
        
        self.status_var = tk.StringVar()
        status_combo = ttk.Combobox(controls_frame, textvariable=self.status_var,
                                values=['', 'Pending', 'Shipped', 'Delivered', 'Cancelled'],
                                state='readonly', width=15)
        status_combo.grid(row=0, column=1, padx=(5, 15))
        
        # Date range
        tk.Label(controls_frame, text="From:", font=self.main_app.FONT_STYLE1,
                bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).grid(row=0, column=2, sticky='w')
        
        self.start_date_var = tk.StringVar()
        start_entry = tk.Entry(controls_frame, textvariable=self.start_date_var,
                            font=self.main_app.FONT_STYLE1, width=12)
        start_entry.grid(row=0, column=3, padx=5)
        tk.Label(controls_frame, text="YYYY-MM-DD", font=(self.main_app.FONT, 8),
                bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).grid(row=1, column=3)
        
        tk.Label(controls_frame, text="To:", font=self.main_app.FONT_STYLE1,
                bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).grid(row=0, column=4, sticky='w')
        
        self.end_date_var = tk.StringVar()
        end_entry = tk.Entry(controls_frame, textvariable=self.end_date_var,
                            font=self.main_app.FONT_STYLE1, width=12)
        end_entry.grid(row=0, column=5, padx=5)
        tk.Label(controls_frame, text="YYYY-MM-DD", font=(self.main_app.FONT, 8),
                bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).grid(row=1, column=5)
        
        # Price range
        tk.Label(controls_frame, text="Price Range:", font=self.main_app.FONT_STYLE1,
                bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).grid(row=2, column=0, sticky='w', pady=(10, 0))
        
        self.min_price_var = tk.StringVar()
        min_price_entry = tk.Entry(controls_frame, textvariable=self.min_price_var,
                                font=self.main_app.FONT_STYLE1, width=10)
        min_price_entry.grid(row=2, column=1, padx=5, pady=(10, 0))
        
        tk.Label(controls_frame, text="to", font=self.main_app.FONT_STYLE1,
                bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).grid(row=2, column=2, pady=(10, 0))
        
        self.max_price_var = tk.StringVar()
        max_price_entry = tk.Entry(controls_frame, textvariable=self.max_price_var,
                                font=self.main_app.FONT_STYLE1, width=10)
        max_price_entry.grid(row=2, column=3, padx=5, pady=(10, 0))
        
        # Filter button
        filter_btn = tk.Button(controls_frame, text="Apply Filters", 
                            font=self.main_app.FONT_STYLE1,
                            command=self.apply_filters)
        filter_btn.grid(row=2, column=4, padx=20, pady=(10, 0))
        
        # Show All button - to test if we can get all orders
        show_all_btn = tk.Button(controls_frame, text="Show All Orders", 
                            font=self.main_app.FONT_STYLE1,
                            command=self.show_all_orders)
        show_all_btn.grid(row=2, column=5, padx=5, pady=(10, 0))
        
        # Clear filters button
        clear_btn = tk.Button(controls_frame, text="Clear Filters", 
                            font=self.main_app.FONT_STYLE1,
                            command=self.clear_filters)
        clear_btn.grid(row=2, column=6, padx=5, pady=(10, 0))

    def show_all_orders(self):
        """Show all orders without any filters"""
        results = self.service.filter_orders()  # Call without any parameters
        
        # Update filtered orders table
        self.filtered_orders_table.delete(*self.filtered_orders_table.get_children())
        for order in results:
            self.filtered_orders_table.insert("", "end", values=(
                order['OrderID'], order['CustomerName'], 
                order['OrderDate'], order['OrderStatus'],
                f"${order['TotalAmount']:.2f}" if order['TotalAmount'] else "$0.00"
            ))
    
    def create_results_section(self):
        # Results notebook
        self.results_notebook = ttk.Notebook(self.parent)
        self.results_notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Customers tab
        self.customers_frame = tk.Frame(self.results_notebook)
        self.results_notebook.add(self.customers_frame, text="Customers")
        self.setup_customers_table()
        
        # Products tab
        self.products_frame = tk.Frame(self.results_notebook)
        self.results_notebook.add(self.products_frame, text="Products")
        self.setup_products_table()
        
        # Orders tab
        self.orders_frame = tk.Frame(self.results_notebook)
        self.results_notebook.add(self.orders_frame, text="Orders")
        self.setup_orders_table()
        
        # Filtered orders tab
        self.filtered_orders_frame = tk.Frame(self.results_notebook)
        self.results_notebook.add(self.filtered_orders_frame, text="Filtered Orders")
        self.setup_filtered_orders_table()
    
    def setup_customers_table(self):
        columns = ("CustomerID", "CustomerName")
        self.customers_table = ttk.Treeview(self.customers_frame, columns=columns, show="headings")
        
        for col in columns:
            self.customers_table.heading(col, text=col)
            self.customers_table.column(col, width=200)
        
        self.customers_table.pack(fill='both', expand=True)
    
    def setup_products_table(self):
        columns = ("ProductID", "ProductName", "Price")
        self.products_table = ttk.Treeview(self.products_frame, columns=columns, show="headings")
        
        for col in columns:
            self.products_table.heading(col, text=col)
            self.products_table.column(col, width=150)
        
        self.products_table.pack(fill='both', expand=True)
    
    def setup_orders_table(self):
        columns = ("OrderID", "CustomerName", "OrderDate", "OrderStatus")
        self.orders_table = ttk.Treeview(self.orders_frame, columns=columns, show="headings")
        
        for col in columns:
            self.orders_table.heading(col, text=col)
            self.orders_table.column(col, width=150)
        
        self.orders_table.pack(fill='both', expand=True)
    
    def setup_filtered_orders_table(self):
        columns = ("OrderID", "CustomerName", "OrderDate", "OrderStatus", "TotalAmount")
        self.filtered_orders_table = ttk.Treeview(self.filtered_orders_frame, columns=columns, show="headings")
        
        for col in columns:
            self.filtered_orders_table.heading(col, text=col)
            self.filtered_orders_table.column(col, width=120)
        
        self.filtered_orders_table.pack(fill='both', expand=True)
    
    def perform_global_search(self):
        search_term = self.search_var.get().strip()
        if not search_term:
            return
        
        results = self.service.global_search(search_term)
        
        # Update customers table
        self.customers_table.delete(*self.customers_table.get_children())
        for customer in results['customers']:
            self.customers_table.insert("", "end", values=(
                customer['CustomerID'], customer['CustomerName']
            ))
        
        # Update products table
        self.products_table.delete(*self.products_table.get_children())
        for product in results['products']:
            self.products_table.insert("", "end", values=(
                product['ProductID'], product['ProductName'], product['Price']
            ))
        
        # Update orders table
        self.orders_table.delete(*self.orders_table.get_children())
        for order in results['orders']:
            self.orders_table.insert("", "end", values=(
                order['OrderID'], order['CustomerName'], 
                order['OrderDate'], order['OrderStatus']
            ))
    
    def apply_filters(self):
        # Get filter values with debug prints
        status = self.status_var.get() if self.status_var.get() else None
        start_date = self.start_date_var.get() if self.start_date_var.get() else None
        end_date = self.end_date_var.get() if self.end_date_var.get() else None
        
        min_price = None
        max_price = None
        try:
            if self.min_price_var.get():
                min_price = float(self.min_price_var.get())
            if self.max_price_var.get():
                max_price = float(self.max_price_var.get())
        except ValueError:
            # Handle invalid price input
            print("Invalid price input")  # Debug
            pass

        # Debug: Print what filters are being applied
        print(f"Applying filters - Status: {status}, Start: {start_date}, End: {end_date}, Min Price: {min_price}, Max Price: {max_price}")  # Debug
        
        results = self.service.filter_orders(
            status=status,
            start_date=start_date,
            end_date=end_date,
            min_price=min_price,
            max_price=max_price
        )
        
        print(f"Filter returned {len(results)} results")  # Debug
        
        # Update filtered orders table
        self.filtered_orders_table.delete(*self.filtered_orders_table.get_children())
        for order in results:
            self.filtered_orders_table.insert("", "end", values=(
                order['OrderID'], order['CustomerName'], 
                order['OrderDate'], order['OrderStatus'],
                f"${order['TotalAmount']:.2f}" if order['TotalAmount'] else "$0.00"
            ))
        
        # If no results, show a message
        if len(results) == 0:
            self.filtered_orders_table.insert("", "end", values=(
                "No orders found", "Try different filters", "", "", ""
            ))
    
    def clear_filters(self):
        self.status_var.set('')
        self.start_date_var.set('')
        self.end_date_var.set('')
        self.min_price_var.set('')
        self.max_price_var.set('')
        self.filtered_orders_table.delete(*self.filtered_orders_table.get_children())