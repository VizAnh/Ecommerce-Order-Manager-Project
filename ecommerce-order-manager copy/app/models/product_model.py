from app.db.connection import get_connection
from mysql.connector import Error

# ==================== PRODUCT ====================

def create_product(pid, pname, price):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("CreateProduct", [pid.upper(), pname, price])
        conn.commit()
        return "Product created successfully."
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def get_product(pid):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("GetProduct", [pid.upper()])
        for result in cursor.stored_results():
            return result.fetchall()
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def update_product(pid, new_name, new_price):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("UpdateProduct", [pid.upper(), new_name, new_price])
        conn.commit()
        return "Product updated successfully."
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def delete_product(pid):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("DeleteProduct", [pid.upper()])
        conn.commit()
        return "Product deleted successfully."
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM products ORDER BY ProductID")
        return cursor.fetchall()
    except Error:
        return []
    finally:
        cursor.close()
        conn.close()