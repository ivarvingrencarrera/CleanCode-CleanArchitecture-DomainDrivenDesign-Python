CREATE SCHEMA IF NOT EXISTS ecommerce;

CREATE TABLE IF NOT EXISTS ecommerce.product (id_product integer, description text, price numeric);

INSERT INTO ecommerce.product(id_product, description, price)
VALUES (1, 'A', 1000),
       (2, 'B', 5000),
       (3, 'C', 30);

CREATE TABLE IF NOT EXISTS ecommerce.coupon (code text, percentage numeric);

INSERT INTO ecommerce.coupon(code, percentage)
VALUES ('VALE20', 20);