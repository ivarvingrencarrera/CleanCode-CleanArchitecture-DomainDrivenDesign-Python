CREATE SCHEMA IF NOT EXISTS ecommerce;

CREATE TABLE IF NOT EXISTS ecommerce.product (id_product integer, description text, price numeric, width integer, height integer, length integer, weight numeric);

INSERT INTO ecommerce.product(id_product, description, price, width, height, length, weight)
VALUES (1, 'A', 1000, 50, 30, 10, 3),
       (2, 'B', 5000, 50, 50, 50, 22),
       (3, 'C', 30, 10, 10, 10, 0.9),
       (4, 'D', 30, -10, 10, 10, 0.9);

CREATE TABLE IF NOT EXISTS ecommerce.coupon (code text, percentage numeric, expire_date timestamp);

INSERT INTO ecommerce.coupon(code, percentage, expire_date)
VALUES ('VALE20', 20, '2023-10-01T10:00:00'),
       ('VALE10', 10, '2022-10-01T10:00:00');