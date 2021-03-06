#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql.err import MySQLError
import hashlib
from flask import g
from stuinfo import app


def connet_db():
    return pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['MYSQL_PASSWORD'],
                           db=app.config['MYSQL_DBNAME'],
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


def get_db():
    if not hasattr(g, 'db'):
        g.db = connet_db()
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


def create_table(drop=False):
    if drop:
        # 删除之前的旧表
        with app.open_resource('drop_table.sql', mode='r') as f:
            exe_script(f.read())

    # 建立新表（若不存在）
    with app.open_resource('schema.sql', mode='r') as f:
        exe_script(f.read())

    # 若没有用户，则添加一个默认用户名
    if no_user():
        create_default_user()

# 在地一个请求之前执行
app.before_first_request(create_table)


def dbfunc(func):
    # 装饰器，自动获取db和cursor并自动销毁cursor
    def wrapper(*args, **kw):
        db = get_db()
        with db.cursor() as cursor:
            return func(db, cursor, *args, **kw)
    return wrapper


@dbfunc
def exe_script(db, cursor, script):
    for sql in script.split(';'):
        try:
            cursor.execute(sql)
        except pymysql.err.InternalError as e:
            # 若查询为空，不应报错
            if e.args[0] != 1065:
                raise e
    db.commit()


@dbfunc
def no_user(db, cursor):
    return cursor.execute('select * from Users') == 0


@dbfunc
def create_default_user(db, cursor):
    username = app.config['DEFAULT_USER']
    md5 = hashlib.md5()
    md5.update(app.config['DEFAULT_PASSWORD'].encode('utf-8'))
    passowrd_md5 = md5.hexdigest()
    cursor.execute('insert into Users values (%s, %s, %s)',
                   [username, passowrd_md5, 'admin'])
    db.commit()


@dbfunc
def check_identity(db, cursor, username, password):
    cursor.execute('select username from Users')
    usernames = [tp['username'] for tp in cursor.fetchall()]
    if username not in usernames:
        return '用户名不存在'
    cursor.execute('select password from Users where username = %s', [username])
    match = cursor.fetchone()['password'] == password
    if not match:
        return '密码错误'
    else:
        return None


@dbfunc
def get_stu_info(db, cursor):
    cursor.execute('select * from Students')
    return cursor.fetchall()


@dbfunc
def add_stu_info(db, cursor, id, name, gender, phonenum=None, emailaddr=None):
    try:
        cursor.execute('insert into Students values (%s, %s, %s, %s, %s)',
                       [id, name, gender, phonenum, emailaddr])
        db.commit()
        # 返回是否成功
        return cursor.rowcount == 1
    except MySQLError:
        return False


@dbfunc
def del_stu_info(db, cursor, id):
    try:
        cursor.execute('delete from Students where id = %s', [id])
        db.commit()
        # 返回是否成功
        return cursor.rowcount == 1
    except MySQLError:
        return False


@dbfunc
def get_stu_name(db, cursor, id):
    cursor.execute('select name from Students where id = %s', [id])
    if cursor.rowcount != 1:
        return None
    else:
        return cursor.fetchone()['name']


@dbfunc
def modify_stu_info(db, cursor, id, phonenum, emailaddr):
    try:
        cursor.execute('update Students set phonenum = %s , emailaddr = %s where id = %s',
                       [phonenum, emailaddr, id])
        db.commit()
        # 返回是否成功
        return cursor.rowcount == 1
    except MySQLError:
        return False


@dbfunc
def modify_user_password(db, cursor, username, old_password, new_password):
    try:
        cursor.execute('update Users set password = %s where username = %s and password = %s',
                       [new_password, username, old_password])
        db.commit()
        # 返回是否成功
        return cursor.rowcount == 1
    except MySQLError:
        return False


@dbfunc
def get_role(db, cursor, username):
    cursor.execute('select role from Users where username = %s', [username])
    if cursor.rowcount != 1:
        return None
    else:
        return cursor.fetchone()['role']


@dbfunc
def get_user_info(db, cursor):
    cursor.execute('select * from Users')
    return cursor.fetchall()


@dbfunc
def create_user(db, cursor, username, password, role):
    try:
        cursor.execute('insert into Users values (%s, %s, %s)',
                       [username, password, role])
        db.commit()
        # 返回是否成功
        return cursor.rowcount == 1
    except MySQLError:
        return False


@dbfunc
def del_user(db, cursor, username):
    try:
        cursor.execute('delete from Users where username = %s', [username])
        db.commit()
        # 返回是否成功
        return cursor.rowcount == 1
    except MySQLError:
        return False


@dbfunc
def modify_user(db, cursor, username, password, role):
    try:
        if username == '':
            query = 'update Users set role = %s where username = %s'
            params = [role, username]
        else:
            query = 'update Users set role = %s , password = %s where username = %s'
            params = [role, password, username]
        cursor.execute(query, params)
        db.commit()
        # 返回是否成功
        return cursor.rowcount == 1
    except MySQLError:
        return False


@dbfunc
def add_course(db, cursor, name):
    try:
        cursor.execute('insert into Courses(name) values (%s)', [name])
        db.commit()
        # 返回是否成功
        return cursor.rowcount == 1
    except MySQLError:
        return False


@dbfunc
def del_course(db, cursor, id):
    try:
        cursor.execute('delete from Courses where id = %s', [id])
        db.commit()
        # 返回是否成功
        return cursor.rowcount == 1
    except MySQLError:
        return False


@dbfunc
def get_courses(db, cursor):
    cursor.execute('select * from Courses')
    return cursor.fetchall()


@dbfunc
def get_course_name(db, cursor, id):
    cursor.execute('select name from Courses where id = %s', [id])
    if cursor.rowcount != 1:
        return None
    else:
        return cursor.fetchone()['name']


@dbfunc
def add_score(db, cursor, stu_id, c_id, score):
    try:
        cursor.execute('insert into Score values (%s, %s, %s)',
                       [stu_id, c_id, score])
        db.commit()
        # 返回是否成功
        return cursor.rowcount == 1
    except MySQLError:
        return False


@dbfunc
def del_score(db, cursor, stu_id, c_id):
    try:
        cursor.execute('delete from Score where stu_id = %s and c_id = %s',
                       [stu_id, c_id])
        db.commit()
        # 返回是否成功
        return cursor.rowcount == 1
    except MySQLError:
        return False


@dbfunc
def modify_score(db, cursor, stu_id, c_id, score):
    try:
        cursor.execute('update Score set score = %s where stu_id = %s and c_id = %s',
                       [score, stu_id, c_id])
        db.commit()
        # 返回是否成功
        return cursor.rowcount == 1
    except MySQLError:
        return False


@dbfunc
def get_score_by_stu_id(db, cursor, stu_id):
    cursor.execute('select id, name, score\
                    from Courses, Score\
                    where Courses.id = c_id and stu_id = %s',
                   [stu_id])
    return cursor.fetchall()


@dbfunc
def get_unselected_course(db, cursor, stu_id):
    cursor.execute('select id, name from Courses\
                    where id not in (\
                        select c_id from Score\
                        where stu_id = %s)',
                   [stu_id])
    return cursor.fetchall()


@dbfunc
def get_score_by_course_id(db, cursor, course_id):
    cursor.execute('select id, name, score\
                    from Students, Score\
                    where Students.id = stu_id and c_id = %s',
                   [course_id])
    return cursor.fetchall()


@dbfunc
def get_unselected_student(db, cursor, course_id):
    cursor.execute('select id, name from Students\
                    where id not in(\
                        select stu_id from Score\
                        where c_id = %s)',
                   [course_id])
    return cursor.fetchall()
