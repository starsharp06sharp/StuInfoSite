#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
import hashlib
from flask import g
from stuinfo import app


def connet_db():
    return mysql.connector.connect(user=app.config['MYSQL_USER'],
                                   password=app.config['MYSQL_PASSWORD'],
                                   database=app.config['MYSQL_DBNAME'])


def get_db():
    if not hasattr(g, 'db'):
        g.db = connet_db()
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


def exe_script(cursor, script):
    for sql in script.split(';'):
        cursor.execute(sql.replace('\n', ''))


def create_table(drop=False):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        if drop:
            # 删除之前的旧表
            with app.open_resource('drop_table.sql', mode='r') as f:
                exe_script(cursor, f.read())
        # 建立新表（若不存在）
        with app.open_resource('schema.sql', mode='r') as f:
            exe_script(cursor, f.read())
        db.commit()
        cursor.close()
        # 若没有用户，则添加一个默认用户名
        create_user_if_no_user(db)


def create_user_if_no_user(db):
    cursor = db.cursor()
    cursor.execute('select * from Users')
    if len(cursor.fetchall()) == 0:
        username = app.config['DEFAULT_USER']
        md5 = hashlib.md5()
        md5.update(app.config['DEFAULT_PASSWORD'].encode('utf-8'))
        passowrd_md5 = md5.hexdigest()
        cursor.execute('insert into Users values (%s, %s)',
                       [username, passowrd_md5])
        db.commit()
    cursor.close()


def check_identity(username, password):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('select username from Users')
        usernames = [tp[0] for tp in cursor.fetchall()]
        if username not in usernames:
            return '用户名不存在'
        cursor.execute(
            'select password from Users where username = %s', [username])
        match = cursor.fetchall()[0][0] == password
        if not match:
            return '密码错误'
        else:
            return None
    finally:
        cursor.close()


def get_stu_info():
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('select * from Students')
    res = cursor.fetchall()
    cursor.close()
    return res


def add_stu_info(id, name, gender, phonenum=None, emailaddr=None):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('insert into Students values (%s, %s, %s, %s, %s)',
                   [id, name, gender, phonenum, emailaddr])
    db.commit()
    success = cursor.rowcount == 1
    cursor.close()
    return success


def del_stu_info(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('delete from Students where id = %s', [id])
    db.commit()
    print(cursor.rowcount)
    success = cursor.rowcount == 1
    cursor.close()
    return success
