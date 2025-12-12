USE eCommerce;

-- 1. Create
DELIMITER $$

CREATE PROCEDURE CreateProduct (
    IN p_ProductID VARCHAR(11),
    IN p_ProductName VARCHAR(255),
    IN p_Price DECIMAL(12,2)
)
BEGIN
    IF p_ProductID NOT REGEXP '^P[0-9]{9}$' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid ProductID format. Expected P#########';
    END IF;

    IF p_ProductName IS NULL OR p_ProductName = '' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'ProductName cannot be empty';
    END IF;

    IF p_Price <= 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Price must be greater than 0';
    END IF;

    IF EXISTS (SELECT 1 FROM products WHERE ProductID = p_ProductID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'ProductID already exists';
    END IF;

    INSERT INTO products (ProductID, ProductName, Price)
    VALUES (p_ProductID, p_ProductName, p_Price);
END$$

DELIMITER ;

-- 2. Read
DELIMITER $$

CREATE PROCEDURE GetProduct (
    IN p_ProductID VARCHAR(11)
)
BEGIN
    SELECT * FROM products
    WHERE ProductID = p_ProductID;
END$$

DELIMITER ;

-- 3. Update
DELIMITER $$

CREATE PROCEDURE UpdateProduct (
    IN p_ProductID VARCHAR(11),
    IN p_NewName VARCHAR(255),
    IN p_NewPrice DECIMAL(12,2)
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM products WHERE ProductID = p_ProductID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'ProductID does not exist';
    END IF;

    IF p_NewName IS NULL OR p_NewName = '' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'ProductName cannot be empty';
    END IF;

    IF p_NewPrice <= 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Price must be greater than 0';
    END IF;

    UPDATE products
    SET ProductName = p_NewName,
        Price = p_NewPrice
    WHERE ProductID = p_ProductID;
END$$

DELIMITER ;

-- 4. Delete
DELIMITER $$

CREATE PROCEDURE DeleteProduct (
    IN p_ProductID VARCHAR(11)
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM products WHERE ProductID = p_ProductID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'ProductID does not exist';
    END IF;

    -- Prevent deletion if product is referenced in quantities (order items)
    IF EXISTS (SELECT 1 FROM quantities WHERE ProductID = p_ProductID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Cannot delete product: It is part of existing orders';
    END IF;

    DELETE FROM products
    WHERE ProductID = p_ProductID;
END$$

DELIMITER ;