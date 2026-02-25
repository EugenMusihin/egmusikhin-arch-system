DROP TABLE IF EXISTS development_plan;

CREATE TABLE development_plan (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(100) NOT NULL
);

INSERT INTO development_plan (id, employee_id, title, status) VALUES
(1, 1, 'Plan 1', 'active'),
(2, 2, 'Plan 2', 'completed'),
(3, 3, 'Plan 3', 'active'),
(4, 4, 'Plan 4', 'draft'),
(5, 5, 'Plan 5', 'active'),
(6, 6, 'Plan 6', 'completed'),
(7, 7, 'Plan 7', 'draft'),
(8, 8, 'Plan 8', 'active'),
(9, 9, 'Plan 9', 'active'),
(10, 10, 'Plan 10', 'completed');

SELECT setval('development_plan_id_seq', (SELECT MAX(id) FROM development_plan));