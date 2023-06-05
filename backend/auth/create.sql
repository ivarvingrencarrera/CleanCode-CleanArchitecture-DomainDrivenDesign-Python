CREATE SCHEMA IF NOT EXISTS ecommerce;

CREATE TABLE IF NOT EXISTS ecommerce.product (id_product integer, description text, price numeric, width integer, height integer, length integer, weight numeric, currency text);

INSERT INTO ecommerce.product(id_product, description, price, width, height, length, weight, currency)
VALUES (1, 'A', 1000, 100, 30, 10, 3, 'BRL'),
       (2, 'B', 5000, 50, 50, 50, 22, 'BRL'),
       (3, 'C', 30, 10, 10, 10, 0.9, 'BRL'),
       (4, 'D', 30, -10, 10, 10, 0.9, 'BRL'),
       (5, 'A', 1000, 50, 30, 10, 3, 'USD');