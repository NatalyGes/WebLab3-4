--
-- Файл сгенерирован с помощью SQLiteStudio v3.2.1 в Пн дек 7 06:01:45 2020
--
-- Использованная кодировка текста: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: tasks
CREATE TABLE tasks (
    id          INTEGER PRIMARY KEY
                        NOT NULL,
    name        TEXT    NOT NULL,
    description TEXT,
    completed   NUMERIC NOT NULL
);


-- Таблица: users
CREATE TABLE users (
    id       INTEGER PRIMARY KEY
                     NOT NULL,
    email    TEXT    NOT NULL,
    password TEXT    NOT NULL
);


-- Таблица: userTask
CREATE TABLE userTask (
    idUser INTEGER NOT NULL,
    idTask INTEGER NOT NULL,
    PRIMARY KEY (
        idUser,
        idTask
    ),
    FOREIGN KEY (
        idUser
    )
    REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (
        idTask
    )
    REFERENCES tasks (id) ON DELETE CASCADE
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
