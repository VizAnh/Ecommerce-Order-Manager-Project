from app.db.connection import get_connection
from mysql.connector import Error

# ==================== QUANTITY ====================

def create_quantity(oid, pid, quantity):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("CreateQuantity", [oid.upper(), pid.upper(), quantity])
        conn.commit()
        return "Quantity created successfully."
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def get_quantity(oid, pid):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("GetQuantity", [oid.upper(), pid.upper()])
        for result in cursor.stored_results():
            return result.fetchall()
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def update_quantity(oid, pid, new_quantity):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("UpdateQuantity", [oid.upper(), pid.upper(), new_quantity])
        conn.commit()
        return "Quantity updated successfully."
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def delete_quantity(oid, pid):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("DeleteQuantity", [oid.upper(), pid.upper()])
        conn.commit()
        return "Quantity deleted successfully."
    except Error as err:
        return f"Error: {err.msg}"
    finally:
        cursor.close()
        conn.close()

def get_all_quantities():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM quantities ORDER BY OrderID")
        return cursor.fetchall()
    except Error:
        return []
    finally:
        cursor.close()
        conn.close()