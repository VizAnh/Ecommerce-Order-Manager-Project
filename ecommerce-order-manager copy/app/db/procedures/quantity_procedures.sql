USE eCommerce;

-- 1. Create
DELIMITER $$

CREATE PROCEDURE CreateQuantity (
    IN p_OrderID VARCHAR(11),
    IN p_ProductID VARCHAR(11),
    IN p_Quantity SMALLINT UNSIGNED
)
BEGIN
    -- Validate quantity > 0
    IF p_Quantity <= 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Quantity must be greater than 0';
    END IF;

    -- Validate order exists
    IF NOT EXISTS (SELECT 1 FROM orders WHERE OrderID = p_OrderID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'OrderID does not exist';
    END IF;

    -- Validate product exists
    IF NOT EXISTS (SELECT 1 FROM products WHERE ProductID = p_ProductID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'ProductID does not exist';
    END IF;

    -- Check duplicate PK (OrderID + ProductID)
    IF EXISTS (
        SELECT 1 FROM quantities 
        WHERE OrderID = p_OrderID AND ProductID = p_ProductID
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'This Order/Product combination already exists';
    END IF;

    INSERT INTO quantities (OrderID, ProductID, Quantity)
    VALUES (p_OrderID, p_ProductID, p_Quantity);
END$$

DELIMITER ;

-- 2. Read
DELIMITER $$

CREATE PROCEDURE GetQuantity (
    IN p_OrderID VARCHAR(11),
    IN p_ProductID VARCHAR(11)
)
BEGIN
    SELECT *
    FROM quantities
    WHERE OrderID = p_OrderID
      AND (p_ProductID = '' OR ProductID = p_ProductID);
END$$

DELIMITER ;

-- 3. Update
DELIMITER $$

CREATE PROCEDURE UpdateQuantity (
    IN p_OrderID VARCHAR(11),
    IN p_ProductID VARCHAR(11),
    IN p_NewQuantity SMALLINT UNSIGNED
)
BEGIN
    IF p_NewQuantity <= 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Quantity must be greater than 0';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM quantities 
        WHERE OrderID = p_OrderID AND ProductID = p_ProductID
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Quantity entry does not exist';
    END IF;

    UPDATE quantities
    SET Quantity = p_NewQuantity
    WHERE OrderID = p_OrderID
      AND ProductID = p_ProductID;
END$$

DELIMITER ;

-- 4. Delete
DELIMITER $$

CREATE PROCEDURE DeleteQuantity (
    IN p_OrderID VARCHAR(11),
    IN p_ProductID VARCHAR(11)
)
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM quantities 
        WHERE OrderID = p_OrderID AND ProductID = p_ProductID
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Quantity entry does not exist';
    END IF;

    DELETE FROM quantities
    WHERE OrderID = p_OrderID
      AND ProductID = p_ProductID;
END$$

DELIMITER ;