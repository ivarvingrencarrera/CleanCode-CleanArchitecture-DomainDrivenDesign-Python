CREATE SCHEMA IF NOT EXISTS ecommerce;

CREATE TABLE IF NOT EXISTS ecommerce.product (id_product integer, description text, price numeric);

INSERT INTO ecommerce.product(id_product, description, price)
VALUES (1, 'A', 1000),
       (2, 'B', 5000),
       (3, 'C', 30);

CREATE TABLE IF NOT EXISTS ecommerce.coupon (code text, percentage numeric, expire_date timestamp);

INSERT INTO ecommerce.coupon(code, percentage, expire_date)
VALUES ('VALE20', 20, '2023-10-01T10:00:00'),
       ('VALE10', 10, '2022-10-01T10:00:00');