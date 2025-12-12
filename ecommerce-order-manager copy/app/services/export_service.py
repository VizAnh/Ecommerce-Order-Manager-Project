import csv
import os
from datetime import datetime
from app.db.connection import get_connection

class ExportService:
    def __init__(self):
        self.export_dir = "exports"
        # Create exports directory if it doesn't exist
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
    
    def export_table_to_csv(self, table_name, filename=None):
        """Export a database table to CSV"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{table_name}_{timestamp}.csv"
        
        filepath = os.path.join(self.export_dir, filename)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Get data from table
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
            
            if not data:
                return False, "No data to export"
            
            # Write to CSV
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                if data:
                    fieldnames = data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
            
            return True, f"Data exported successfully to {filename}"
            
        except Exception as e:
            return False, f"Export failed: {str(e)}"
        finally:
            cursor.close()
            conn.close()
    
    def export_customers(self):
        """Export customers data"""
        return self.export_table_to_csv("customers")
    
    def export_products(self):
        """Export products data"""
        return self.export_table_to_csv("products")
    
    def export_orders(self):
        """Export orders data"""
        return self.export_table_to_csv("orders")
    
    def export_quantities(self):
        """Export quantities data"""
        return self.export_table_to_csv("quantities")
    
    def export_orders_with_details(self):
        """Export orders with customer names and calculated totals"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"orders_detailed_{timestamp}.csv"
        filepath = os.path.join(self.export_dir, filename)
        
        try:
            query = """
            SELECT 
                o.OrderID,
                c.CustomerName,
                o.OrderDate,
                o.OrderStatus,
                SUM(q.Quantity * p.Price) as TotalAmount,
                COUNT(q.ProductID) as TotalItems
            FROM orders o
            LEFT JOIN customers c ON o.CustomerID = c.CustomerID
            LEFT JOIN quantities q ON o.OrderID = q.OrderID
            LEFT JOIN products p ON q.ProductID = p.ProductID
            GROUP BY o.OrderID, c.CustomerName, o.OrderDate, o.OrderStatus
            ORDER BY o.OrderDate DESC
            """
            
            cursor.execute(query)
            data = cursor.fetchall()
            
            if not data:
                return False, "No order data to export"
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                if data:
                    fieldnames = data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
            
            return True, f"Orders with details exported to {filename}"
            
        except Exception as e:
            return False, f"Export failed: {str(e)}"
        finally:
            cursor.close()
            conn.close()
    
    def export_sales_report(self):
        """Export sales report with revenue by product"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sales_report_{timestamp}.csv"
        filepath = os.path.join(self.export_dir, filename)
        
        try:
            query = """
            SELECT 
                p.ProductID,
                p.ProductName,
                p.Price,
                SUM(q.Quantity) as TotalSold,
                SUM(q.Quantity * p.Price) as TotalRevenue,
                COUNT(DISTINCT q.OrderID) as NumberOfOrders
            FROM products p
            LEFT JOIN quantities q ON p.ProductID = q.ProductID
            LEFT JOIN orders o ON q.OrderID = o.OrderID AND o.OrderStatus = 'Delivered'
            GROUP BY p.ProductID, p.ProductName, p.Price
            ORDER BY TotalRevenue DESC
            """
            
            cursor.execute(query)
            data = cursor.fetchall()
            
            if not data:
                return False, "No sales data to export"
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                if data:
                    fieldnames = data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
            
            return True, f"Sales report exported to {filename}"
            
        except Exception as e:
            return False, f"Export failed: {str(e)}"
        finally:
            cursor.close()
            conn.close()
    
    def get_export_files(self):
        """Get list of exported files"""
        if not os.path.exists(self.export_dir):
            return []
        
        files = []
        for filename in os.listdir(self.export_dir):
            if filename.endswith('.csv'):
                filepath = os.path.join(self.export_dir, filename)
                stat = os.stat(filepath)
                files.append({
                    'name': filename,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # Sort by modification time, newest first
        files.sort(key=lambda x: x['modified'], reverse=True)
        return files