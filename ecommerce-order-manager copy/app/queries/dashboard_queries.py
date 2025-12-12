# KPI Queries
GET_TOTAL_CUSTOMERS = "SELECT COUNT(*) as total_customers FROM customers"
GET_TOTAL_PRODUCTS = "SELECT COUNT(*) as total_products FROM products"
GET_ORDERS_BY_STATUS = """
    SELECT OrderStatus, COUNT(*) as count 
    FROM orders 
    GROUP BY OrderStatus
"""
GET_REVENUE_TO_DATE = """
    SELECT SUM(q.Quantity * p.Price) as revenue
    FROM quantities q
    JOIN products p ON q.ProductID = p.ProductID
    JOIN orders o ON q.OrderID = o.OrderID
    WHERE o.OrderStatus = 'Delivered'
"""

# Chart Queries
GET_REVENUE_BY_DAY = """
    SELECT DATE(o.OrderDate) as date, SUM(q.Quantity * p.Price) as revenue
    FROM quantities q
    JOIN products p ON q.ProductID = p.ProductID
    JOIN orders o ON q.OrderID = o.OrderID
    WHERE o.OrderStatus = 'Delivered'
    GROUP BY DATE(o.OrderDate)
    ORDER BY date DESC
    LIMIT 30
"""

GET_REVENUE_BY_WEEK = """
    SELECT YEARWEEK(o.OrderDate) as week, SUM(q.Quantity * p.Price) as revenue
    FROM quantities q
    JOIN products p ON q.ProductID = p.ProductID
    JOIN orders o ON q.OrderID = o.OrderID
    WHERE o.OrderStatus = 'Delivered'
    GROUP BY YEARWEEK(o.OrderDate)
    ORDER BY week DESC
    LIMIT 12
"""

GET_REVENUE_BY_MONTH = """
    SELECT DATE_FORMAT(o.OrderDate, '%Y-%m') as month, SUM(q.Quantity * p.Price) as revenue
    FROM quantities q
    JOIN products p ON q.ProductID = p.ProductID
    JOIN orders o ON q.OrderID = o.OrderID
    WHERE o.OrderStatus = 'Delivered'
    GROUP BY DATE_FORMAT(o.OrderDate, '%Y-%m')
    ORDER BY month DESC
    LIMIT 12
"""

GET_TOP_PRODUCTS_BY_REVENUE = """
    SELECT p.ProductID, p.ProductName, SUM(q.Quantity * p.Price) as revenue
    FROM quantities q
    JOIN products p ON q.ProductID = p.ProductID
    JOIN orders o ON q.OrderID = o.OrderID
    WHERE o.OrderStatus = 'Delivered'
    GROUP BY p.ProductID, p.ProductName
    ORDER BY revenue DESC
    LIMIT %s
"""

# Search Queries
SEARCH_CUSTOMERS = """
    SELECT CustomerID, CustomerName 
    FROM customers 
    WHERE CustomerName LIKE %s
"""

SEARCH_PRODUCTS = """
    SELECT ProductID, ProductName, Price 
    FROM products 
    WHERE ProductName LIKE %s
"""

SEARCH_ORDERS = """
    SELECT o.OrderID, c.CustomerName, o.OrderDate, o.OrderStatus
    FROM orders o
    JOIN customers c ON o.CustomerID = c.CustomerID
    WHERE o.OrderID LIKE %s OR c.CustomerName LIKE %s
"""

FILTER_ORDERS_BASE = """
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