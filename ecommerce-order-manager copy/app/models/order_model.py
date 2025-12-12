from app.db.connection import get_connection
from mysql.connector import Error

# ==================== ORDER ====================

def create_order(oid, cid, odate, ostatus):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("CreateOrder", [oid.upper(), cid.upper(), odate, ostatus])
        conn.commit()
        return "Order created successfully."
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def get_order(oid):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("GetOrder", [oid.upper()])
        for result in cursor.stored_results():
            return result.fetchall()
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def update_order(oid, new_cid, new_date, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("UpdateOrder", [oid.upper(), new_cid.upper(), new_date, new_status])
        conn.commit()
        return "Order updated successfully."
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def delete_order(oid):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("CascadeDeleteOrder", [oid.upper()])
        conn.commit()
        return "Order deleted successfully."
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def get_all_orders():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM orders ORDER BY OrderID")
        return cursor.fetchall()
    except Error:
        return []
    finally:
        cursor.close()
        conn.close()