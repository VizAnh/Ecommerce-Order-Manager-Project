from app.db.connection import get_connection
from app.queries.dashboard_queries import *

class DashboardService:
    @staticmethod
    def get_kpis():
        """Get all KPIs for dashboard"""
        conn = get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                # Total customers
                cursor.execute(GET_TOTAL_CUSTOMERS)
                total_customers = cursor.fetchone()['total_customers']
                
                # Total products
                cursor.execute(GET_TOTAL_PRODUCTS)
                total_products = cursor.fetchone()['total_products']
                
                # Orders by status
                cursor.execute(GET_ORDERS_BY_STATUS)
                orders_by_status = cursor.fetchall()
                
                # Revenue to date
                cursor.execute(GET_REVENUE_TO_DATE)
                revenue_result = cursor.fetchone()
                revenue_to_date = revenue_result['revenue'] if revenue_result else 0
                
                return {
                    'total_customers': total_customers,
                    'total_products': total_products,
                    'orders_by_status': orders_by_status,
                    'revenue_to_date': float(revenue_to_date) if revenue_to_date else 0
                }
        finally:
            conn.close()
    
    @staticmethod
    def get_revenue_by_period(period='day'):
        """Get revenue by day/week/month"""
        conn = get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                if period == 'day':
                    cursor.execute(GET_REVENUE_BY_DAY)
                elif period == 'week':
                    cursor.execute(GET_REVENUE_BY_WEEK)
                else:  # month
                    cursor.execute(GET_REVENUE_BY_MONTH)
                
                return cursor.fetchall()
        finally:
            conn.close()
    
    @staticmethod
    def get_top_products_by_revenue(limit=10):
        """Get top N products by revenue"""
        conn = get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_TOP_PRODUCTS_BY_REVENUE, (limit,))
                return cursor.fetchall()
        finally:
            conn.close()

class SearchService:
    @staticmethod
    def global_search(search_term):
        """Global search across customers, products, and orders"""
        conn = get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                # Search customers
                cursor.execute(SEARCH_CUSTOMERS, (f"%{search_term}%",))
                customers = cursor.fetchall()
                
                # Search products
                cursor.execute(SEARCH_PRODUCTS, (f"%{search_term}%",))
                products = cursor.fetchall()
                
                # Search orders - note: two parameters for the OR condition
                cursor.execute(SEARCH_ORDERS, (f"%{search_term}%", f"%{search_term}%"))
                orders = cursor.fetchall()
                
                return {
                    'customers': customers,
                    'products': products,
                    'orders': orders
                }
        finally:
            conn.close()
    
    @staticmethod
    def filter_orders(status=None, start_date=None, end_date=None, min_price=None, max_price=None):
        """Filter orders with various criteria"""
        conn = get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                # Modified query to handle ONLY_FULL_GROUP_BY
                query = """
                    SELECT 
                        o.OrderID,
                        c.CustomerName,
                        o.OrderDate,
                        o.OrderStatus,
                        SUM(q.Quantity * p.Price) as TotalAmount
                    FROM orders o
                    JOIN customers c ON o.CustomerID = c.CustomerID
                    JOIN quantities q ON o.OrderID = q.OrderID
                    JOIN products p ON q.ProductID = p.ProductID
                """
                params = []
                
                # Build WHERE conditions
                conditions = []
                if status:
                    conditions.append("o.OrderStatus = %s")
                    params.append(status)
                if start_date:
                    conditions.append("o.OrderDate >= %s")
                    params.append(start_date)
                if end_date:
                    conditions.append("o.OrderDate <= %s")
                    params.append(end_date)
                
                # Add WHERE clause if conditions exist
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                
                # Always add GROUP BY with all non-aggregated columns
                query += " GROUP BY o.OrderID, c.CustomerName, o.OrderDate, o.OrderStatus"
                
                # Build HAVING conditions for price filtering
                price_conditions = []
                if min_price is not None:
                    price_conditions.append("SUM(q.Quantity * p.Price) >= %s")
                    params.append(min_price)
                if max_price is not None:
                    price_conditions.append("SUM(q.Quantity * p.Price) <= %s")
                    params.append(max_price)
                
                # Add HAVING clause if price conditions exist
                if price_conditions:
                    query += " HAVING " + " AND ".join(price_conditions)
                
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            conn.close()