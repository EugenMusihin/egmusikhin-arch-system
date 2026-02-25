-- Удаляем таблицу если существует
DROP TABLE IF EXISTS plans;

-- Создаем таблицу
CREATE TABLE plans (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(100) NOT NULL
);

-- Вставляем 10 записей (id 1-10)
INSERT INTO plans (id, employee_id, title, status) VALUES
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

-- Обновляем sequence чтобы POST работал корректно
SELECT setval('plans_id_seq', (SELECT MAX(id) FROM plans));