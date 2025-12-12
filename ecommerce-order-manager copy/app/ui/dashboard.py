import tkinter as tk
from tkinter import ttk
from app.services.dashboard_service import DashboardService
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Dashboard:
    def __init__(self, parent_frame, main_app):
        self.parent = parent_frame
        self.main_app = main_app
        self.service = DashboardService()
        
    def show(self):
        # Clear existing widgets
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Create dashboard layout
        self.create_kpi_section()
        self.create_charts_section()
        
    def create_kpi_section(self):
        # KPI Frame
        kpi_frame = tk.Frame(self.parent, bg=self.main_app.COLOUR3)
        kpi_frame.pack(fill='x', padx=20, pady=10)
        
        # Get KPI data
        kpis = self.service.get_kpis()
        
        # KPI Cards
        cards_data = [
            ("Total Customers", kpis['total_customers'], self.main_app.COLOUR2),
            ("Total Products", kpis['total_products'], self.main_app.COLOUR2),
            ("Revenue to Date", f"${kpis['revenue_to_date']:,.2f}", self.main_app.COLOUR2),
        ]
        
        for i, (title, value, color) in enumerate(cards_data):
            card = tk.Frame(kpi_frame, bg=color, relief='raised', bd=2)
            card.grid(row=0, column=i, padx=10, pady=5, sticky='ew')
            kpi_frame.columnconfigure(i, weight=1)
            
            tk.Label(card, text=title, font=(self.main_app.FONT, 12, 'bold'), 
                    bg=color, fg=self.main_app.COLOUR5).pack(pady=(10, 5))
            tk.Label(card, text=str(value), font=(self.main_app.FONT, 16, 'bold'), 
                    bg=color, fg=self.main_app.COLOUR5).pack(pady=(0, 10))
        
        # Orders by status
        status_frame = tk.Frame(kpi_frame, bg=self.main_app.COLOUR2, relief='raised', bd=2)
        status_frame.grid(row=0, column=3, padx=10, pady=5, sticky='ew')
        
        tk.Label(status_frame, text="Orders by Status", font=(self.main_app.FONT, 12, 'bold'),
                bg=self.main_app.COLOUR2, fg=self.main_app.COLOUR5).pack(pady=(10, 5))
        
        for status in kpis['orders_by_status']:
            text = f"{status['OrderStatus']}: {status['count']}"
            tk.Label(status_frame, text=text, font=(self.main_app.FONT, 10),
                    bg=self.main_app.COLOUR2, fg=self.main_app.COLOUR5).pack()
    
    def create_charts_section(self):
        # Charts Frame
        charts_frame = tk.Frame(self.parent, bg=self.main_app.COLOUR4)
        charts_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left chart - Revenue by period
        left_chart_frame = tk.Frame(charts_frame, bg=self.main_app.COLOUR3)
        left_chart_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Period selector
        period_frame = tk.Frame(left_chart_frame, bg=self.main_app.COLOUR3)
        period_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(period_frame, text="View by:", font=self.main_app.FONT_STYLE1,
                bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5).pack(side='left')
        
        period_var = tk.StringVar(value='day')
        periods = [('Day', 'day'), ('Week', 'week'), ('Month', 'month')]
        
        for text, value in periods:
            tk.Radiobutton(period_frame, text=text, variable=period_var, value=value,
                          command=lambda: self.update_revenue_chart(period_var.get(), chart_canvas),
                          bg=self.main_app.COLOUR3, fg=self.main_app.COLOUR5,
                          font=self.main_app.FONT_STYLE1).pack(side='left', padx=5)
        
        # Chart container
        chart_container = tk.Frame(left_chart_frame, bg='white')
        chart_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create initial chart
        fig, ax = plt.subplots(figsize=(6, 4))
        canvas = FigureCanvasTkAgg(fig, chart_container)
        chart_canvas = canvas.get_tk_widget()
        chart_canvas.pack(fill='both', expand=True)
        
        # Right chart - Top products
        right_chart_frame = tk.Frame(charts_frame, bg=self.main_app.COLOUR3)
        right_chart_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        tk.Label(right_chart_frame, text="Top Products by Revenue", 
                font=(self.main_app.FONT, 14, 'bold'), bg=self.main_app.COLOUR3, 
                fg=self.main_app.COLOUR5).pack(pady=10)
        
        # Products chart container
        products_container = tk.Frame(right_chart_frame, bg='white')
        products_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create products chart
        self.create_top_products_chart(products_container)
        
        # Initial chart update
        self.update_revenue_chart('day', chart_canvas)
    
    def update_revenue_chart(self, period, canvas_widget):
        data = self.service.get_revenue_by_period(period)
        
        # Clear previous chart
        for widget in canvas_widget.winfo_children():
            widget.destroy()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        if data:
            dates = [item[list(item.keys())[0]] for item in data]
            revenues = [float(item['revenue']) for item in data]
            
            ax.bar(range(len(dates)), revenues, color=self.main_app.COLOUR4)
            ax.set_ylabel('Revenue ($)')
            ax.set_xlabel('Period')
            ax.set_title(f'Revenue by {period.capitalize()}')
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)
            plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, canvas_widget)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def create_top_products_chart(self, parent):
        data = self.service.get_top_products_by_revenue(10)
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        if data:
            products = [item['ProductName'][:15] + '...' if len(item['ProductName']) > 15 else item['ProductName'] 
                       for item in data]
            revenues = [float(item['revenue']) for item in data]
            
            ax.barh(products, revenues, color=self.main_app.COLOUR4)
            ax.set_xlabel('Revenue ($)')
            ax.set_title('Top Products by Revenue')
            plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)