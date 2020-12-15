# coding=utf-8
import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash, generate_password_hash
from entities import User, Task

# Подключаемся к БД, для дальнейшего полученяия инфы
db_path = '/'.join([str(Path(__file__).parent), '..', 'db', 'database.sqlite'])
db = sqlite3.connect(db_path, check_same_thread=False)

# генерим хэш для пароля лр 3
class Storage:
    @staticmethod
    def add_user(user:User):
        """объявление пользователя
        :param user:    новый пользователь
        :type user:     User"""
        db.execute('INSERT INTO users (email, password) VALUES (?, ?)',
                   (user.email, generate_password_hash(user.password)))
        db.commit()

    @staticmethod
    def get_user_by_email_and_password(email: str, passwordHash: str):
        """Найти пользователя по email и паролю
        :param email:       электронная почта
        :type email:        str
        :param passwordHash:    хэш пароля
        :type passwordHash:     str
        :return: пользователь
        :rtype: User
        """
        user_data = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        if user_data and check_password_hash(user_data[2], passwordHash):
            return User(id=user_data[0], email=user_data[1], password=user_data[2])
        else:
            return None

    @staticmethod
    def get_user_by_id(id: int):
        """Найти пользователя по id (добавить пользователя в класс)
        :param id:  идентификатор пользователя
        :type id:   int
        :return:    пользователь
        :rtype:     User"""
        user_data = db.execute('SELECT * FROM users WHERE id=?', (id,)).fetchone()
        if user_data:
            return User(id=user_data[0], email=user_data[1], password=user_data[2])
        else:
            return None

    @staticmethod
    def is_user_registred(email: str) -> bool:
        """Проверка есть ли уже пользователь с таким email
        :param email:       электронная почта
        :type email:        str
        :return:    True/False
        :rtype:     Boolean"""
        user_data = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        if user_data:
            return True
        else:
            return False

    @staticmethod
    def get_task_by_id(id):
        """"найти задачи пользоваиеля"""
        task_data = db.execute(
            'SELECT t.id, t.name, t.description, t.completed FROM users u, tasks t, userTask ut WHERE t.id = ut.idTask '
            'and u.id = ut.idUser and u.id = ?', (id,)).fetchall()
        if task_data:
            return task_data
        else:
            return None

    @staticmethod
    def del_task(user_id, task_id):
        """"удалить задачу пользоваиеля"""
        db.execute('DELETE FROM userTask WHERE idUser = ? and idTask = ?', (user_id, task_id))
        db.commit()

    @staticmethod
    def add_task(task, user_id):
        """"добавить задачу пользоваиеля"""
        cursor = db.cursor()
        cursor.execute('INSERT INTO tasks (name, description) VALUES (?, ?)', (task.name, task.description))
        new_id = cursor.lastrowid
        cursor.execute('INSERT INTO userTask (idUser, idTask) VALUES (?, ?)', (user_id, new_id))
        db.commit()

    @staticmethod
    def update_task_status(task_id, action):
        """"изменить состояние задачи"""
        if action == "completed":
            db.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
            db.commit()
        if action == "uncompleted":
            db.execute('UPDATE tasks SET completed = 0 WHERE id = ?', (task_id,))
            db.commit()

    @staticmethod
    def get_task_status(task_id):
        """"добавить задачу в класс"""
        task_status = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        if task_status:
            return Task(task_status[0], task_status[1], task_status[2], task_status[3])
        else:
            return None


    @staticmethod
    def find_task(task_id):
        """"найти задачу пальзователя"""
        change_task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        if change_task:
            return Task(id=change_task[0], name=change_task[1], description=change_task[2], status=change_task[3])
        else:
            return None

    @staticmethod
    def update_task(task_id, task_name, task_description):
        """"изменить задачу пользователя"""
        db.execute('UPDATE tasks SET name = ?, description = ? WHERE id = ?', (task_name, task_description, task_id,))
        db.commit()
