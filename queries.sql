-- Reporting queries

SELECT * FROM users;                                          -- SELECT *, no LIMIT

DELETE FROM orders;                                           -- missing WHERE
UPDATE users SET role = 'admin';                              -- missing WHERE

SELECT u.name, o.total FROM users u, orders o;                -- implicit cross join

SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM banned);   -- NOT IN breaks when user_id has NULLs

SELECT * FROM users WHERE deleted_at = NULL;                  -- never true, use IS NULL

SELECT * FROM users WHERE email LIKE '%@example.com';         -- leading wildcard, no index

SELECT * FROM logs WHERE DATE(created_at) = '2026-10-12';     -- function on a column defeats the index

SELECT name, COUNT(*) FROM users;                             -- non-aggregated column without GROUP BY

SELECT * FROM events ORDER BY id LIMIT 10 OFFSET 1000000;     -- deep OFFSET pagination

SELECT name FROM a UNION SELECT name FROM b;                  -- UNION sorts and dedupes, UNION ALL may be intended

SELECT * FROM orders LIMIT 10;                                -- LIMIT without ORDER BY

SELECT * FROM users u LEFT JOIN orders o ON o.user_id = u.id WHERE o.total > 10;   -- WHERE turns LEFT JOIN into INNER

CREATE TABLE payments (
  id INT,                                                     -- no primary key
  user_id INT,                                                -- no foreign key
  amount FLOAT,                                               -- float for money
  paid_at VARCHAR(20),                                        -- date stored as a string
  card_number VARCHAR(19),                                    -- raw card number
  password VARCHAR(50)                                        -- plaintext password
);

DROP TABLE users;                                             -- no IF EXISTS, no backup
GRANT ALL PRIVILEGES ON *.* TO 'app'@'%' IDENTIFIED BY 'admin123';   -- over-broad grant, hardcoded password

BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- missing second UPDATE and no COMMIT or ROLLBACK
