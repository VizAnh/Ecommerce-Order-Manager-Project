CREATE DATABASE IF NOT EXISTS eCommerce;
USE eCommerce;

-- Recreate table if exist
DROP TABLE IF EXISTS quantities;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- Create table
CREATE TABLE customers (
    CustomerID VARCHAR(11) NOT NULL,
    CustomerName VARCHAR(255) NOT NULL,
    CONSTRAINT chk_customerid_format CHECK (CustomerID REGEXP '^C[0-9]{9}$'),
    PRIMARY KEY (CustomerID)
);

CREATE TABLE products (
    ProductID VARCHAR(11) NOT NULL,
    ProductName VARCHAR(255) NOT NULL,
    Price DECIMAL(12 , 2 ) NOT NULL,
    CONSTRAINT chk_productid_format CHECK (ProductID REGEXP '^P[0-9]{9}$'),
    CONSTRAINT chk_price CHECK (Price > 0),
    PRIMARY KEY (ProductID)
);

CREATE TABLE orders (
    OrderID VARCHAR(11) NOT NULL,
    CustomerID VARCHAR(11) DEFAULT NULL,
    OrderDate DATE NOT NULL,
    OrderStatus ENUM('Pending', 'Shipped', 'Delivered', 'Cancelled') NOT NULL,
    CONSTRAINT chk_orderid_format CHECK (OrderID REGEXP '^O[0-9]{9}$'),
    PRIMARY KEY (OrderID),
    FOREIGN KEY (CustomerID)
        REFERENCES customers (CustomerID)
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE quantities (
    OrderID VARCHAR(11) NOT NULL,
    ProductID VARCHAR(11) NOT NULL,
    Quantity SMALLINT UNSIGNED NOT NULL,
    PRIMARY KEY (OrderID , ProductID),
    FOREIGN KEY (OrderID)
        REFERENCES orders (OrderID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ProductID)
        REFERENCES products (ProductID)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_quantity CHECK (Quantity > 0)
);
