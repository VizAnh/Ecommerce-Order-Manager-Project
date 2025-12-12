from app.db.connection import get_connection
from mysql.connector import Error

# ==================== CUSTOMER ====================

def create_customer(cid, cname):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("CreateCustomer", [cid.upper(), cname])
        conn.commit()
        return "Customer created successfully."
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def get_customer(cid):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("GetCustomer", [cid.upper()])
        for result in cursor.stored_results():
            return result.fetchall()
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def update_customer(cid, new_name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("UpdateCustomer", [cid.upper(), new_name])
        conn.commit()
        return "Customer updated successfully."
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def delete_customer(cid):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("CascadeDeleteCustomer", [cid.upper()])
        conn.commit()
        return "Customer deleted successfully."
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM customers ORDER BY CustomerID")
        return cursor.fetchall()
    except Error:
        return []
    finally:
        cursor.close()
        conn.close()