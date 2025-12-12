USE eCommerce;

-- 1. Create
DELIMITER $$

CREATE PROCEDURE CreateCustomer (
    IN p_CustomerID VARCHAR(11),
    IN p_CustomerName VARCHAR(255)
)
BEGIN
    -- Validate ID format
    IF p_CustomerID NOT REGEXP '^C[0-9]{9}$' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid CustomerID format. Expected C#########';
    END IF;

    -- Validate name
    IF p_CustomerName IS NULL OR p_CustomerName = '' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'CustomerName cannot be empty';
    END IF;

    -- Check if ID already exists
    IF EXISTS (SELECT 1 FROM customers WHERE CustomerID = p_CustomerID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'CustomerID already exists';
    END IF;

    INSERT INTO customers (CustomerID, CustomerName)
    VALUES (p_CustomerID, p_CustomerName);
END$$

DELIMITER ;

-- 2. Read
DELIMITER $$

CREATE PROCEDURE GetCustomer(
    IN p_CustomerID VARCHAR(11)
)
BEGIN
    SELECT * FROM customers
    WHERE CustomerID = p_CustomerID;
END$$

DELIMITER ;

-- 3. Update
DELIMITER $$

CREATE PROCEDURE UpdateCustomer (
    IN p_CustomerID VARCHAR(11),
    IN p_NewName VARCHAR(255)
)
BEGIN
    -- Validate existence
    IF NOT EXISTS (SELECT 1 FROM customers WHERE CustomerID = p_CustomerID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'CustomerID does not exist';
    END IF;

    -- Validate new name
    IF p_NewName IS NULL OR p_NewName = '' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'CustomerName cannot be empty';
    END IF;

    UPDATE customers
    SET CustomerName = p_NewName
    WHERE CustomerID = p_CustomerID;
END$$

DELIMITER ;

-- 4. Delete
DELIMITER $$

CREATE PROCEDURE CascadeDeleteCustomer (
    IN p_CustomerID VARCHAR(11)
)
BEGIN
    DECLARE exit handler FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'CascadeDeleteCustomer failed, rolled back';
    END;

    START TRANSACTION;

    -- Validate existence
    IF NOT EXISTS (SELECT 1 FROM customers WHERE CustomerID = p_CustomerID) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'CustomerID does not exist';
    END IF;

    -- Delete quantities of all orders belonging to the customer
    DELETE q FROM quantities q
    JOIN orders o ON q.OrderID = o.OrderID
    WHERE o.CustomerID = p_CustomerID;

    -- Delete orders
    DELETE FROM orders WHERE CustomerID = p_CustomerID;

    -- Delete customer
    DELETE FROM customers WHERE CustomerID = p_CustomerID;

    COMMIT;
END$$

DELIMITER ;
