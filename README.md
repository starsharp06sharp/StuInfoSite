#student info website
课程设计

##启动方法

###安装依赖

```bash
sudo apt-get install python3 python3-pip mysql-server mysql-client
pip3 install PyMySQL Flask
```

###~~初始化数据库~~
~~在mysql中创建一个叫`stuinfo`的数据库，然后执行`./create_table.py`~~  
如需删除所有数据重新创建，执行`./create_table.py --drop`

###启动测试服务器
运行`./start_debug_server.py`

###生产服务器
目前使用uwsgi，运行`sudo uwsgi uwsgi.ini`即可