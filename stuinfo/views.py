#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request, redirect, url_for, abort, render_template, flash, session
from stuinfo import app, db
import json


@app.route('/', methods=['GET'])
def index():
    if not session.get('logged_in_user'):
        return redirect(url_for('login'))
    return render_template('index.html', students=db.get_stu_info())


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        error = db.check_identity(
            request.form['username'], request.form['password'])
        if error is None:
            session['logged_in_user'] = request.form['username']
            flash('登录成功', 'success')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('logged_in_user', None)
    return redirect(url_for('login'))


@app.route('/add', methods=['POST'])
def add_student():
    if not session.get('logged_in_user'):
        abort(403)
    success = db.add_stu_info(request.form['id'], request.form['name'],
                              request.form['gender'], request.form['phonenum'],
                              request.form['emailaddr'])
    if success:
        flash('添加成功', 'success')
    else:
        flash('添加失败', 'error')
    return redirect(url_for('index'))


@app.route('/delete/<student_id>', methods=['GET'])
def delete_student(student_id):
    if not session.get('logged_in_user'):
        abort(403)
    success = db.del_stu_info(student_id)
    if success:
        flash('删除成功', 'success')
    else:
        flash('删除失败', 'error')
    return redirect(url_for('index'))
