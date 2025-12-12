USE eCommerce;

-- 1. Create
DELIMITER $$

CREATE PROCEDURE CreateOrder (
    IN p_OrderID VARCHAR(11),
    IN p_CustomerID VARCHAR(11),
    IN p_OrderDate DATE,
    IN p_OrderStatus ENUM('Pending', 'Shipped', 'Delivered', 'Cancelled')
)
BEGIN
    IF p_OrderID NOT REGEXP '^O[0-9]{9}$' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid OrderID format. Expected O#########';
    END IF;

    -- Validate customer exists
    IF NOT EXISTS (SELECT 1 FROM customers WHERE CustomerID = p_CustomerID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'CustomerID does not exist';
    END IF;

    IF p_OrderDate IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'OrderDate cannot be NULL';
    END IF;

    IF EXISTS (SELECT 1 FROM orders WHERE OrderID = p_OrderID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'OrderID already exists';
    END IF;

    INSERT INTO orders (OrderID, CustomerID, OrderDate, OrderStatus)
    VALUES (p_OrderID, p_CustomerID, p_OrderDate, p_OrderStatus);
END$$

DELIMITER ;

-- 2. Read
DELIMITER $$

CREATE PROCEDURE GetOrder (
    IN p_OrderID VARCHAR(11)
)
BEGIN
    SELECT * FROM orders
    WHERE OrderID = p_OrderID;
END$$

DELIMITER ;

-- 3. Update
DELIMITER $$

CREATE PROCEDURE UpdateOrder (
    IN p_OrderID VARCHAR(11),
    IN p_NewCustomerID VARCHAR(11),
    IN p_NewOrderDate DATE,
    IN p_NewStatus ENUM('Pending', 'Shipped', 'Delivered', 'Cancelled')
)
BEGIN
    -- Order exists?
    IF NOT EXISTS (SELECT 1 FROM orders WHERE OrderID = p_OrderID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'OrderID does not exist';
    END IF;

    -- Customer exists?
    IF NOT EXISTS (SELECT 1 FROM customers WHERE CustomerID = p_NewCustomerID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'New CustomerID does not exist';
    END IF;

    IF p_NewOrderDate IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'OrderDate cannot be NULL';
    END IF;

    UPDATE orders
    SET CustomerID = p_NewCustomerID,
        OrderDate = p_NewOrderDate,
        OrderStatus = p_NewStatus
    WHERE OrderID = p_OrderID;
END$$

DELIMITER ;

-- 4. Delete
DELIMITER $$

CREATE PROCEDURE CascadeDeleteOrder (
    IN p_OrderID VARCHAR(11)
)
BEGIN
    DECLARE exit handler FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'CascadeDeleteOrder failed, rolled back';
    END;

    START TRANSACTION;

    -- Validate existence
    IF NOT EXISTS (SELECT 1 FROM orders WHERE OrderID = p_OrderID) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'OrderID does not exist';
    END IF;

    -- Delete quantities
    DELETE FROM quantities WHERE OrderID = p_OrderID;

    -- Delete order
    DELETE FROM orders WHERE OrderID = p_OrderID;

    COMMIT;
END$$

DELIMITER ;