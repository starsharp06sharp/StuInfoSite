#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
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
    with app.app_context():
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
            cursor.execute(sql.replace('\n', ''))
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
    cursor.execute('insert into Users values (%s, %s)', (username, passowrd_md5))
    db.commit()


@dbfunc
def check_identity(db, cursor, username, password):
    cursor.execute('select username from Users')
    usernames = [tp['username'] for tp in cursor.fetchall()]
    if username not in usernames:
        return '用户名不存在'
    cursor.execute('select password from Users where username = %s', (username,))
    match = cursor.fetchall()[0]['password'] == password
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
    cursor.execute('insert into Students values (%s, %s, %s, %s, %s)',
                   [id, name, gender, phonenum, emailaddr])
    db.commit()
    # 返回是否成功
    return cursor.rowcount == 1


@dbfunc
def del_stu_info(db, cursor, id):
    cursor.execute('delete from Students where id = %s', [id])
    db.commit()
    # 返回是否成功
    return cursor.rowcount == 1
