#student info website
课程设计

##启动方法

###安装依赖

```bash
sudo apt-get install python3 python3-pip mysql-server mysql-client
pip3 install PyMySQL Flask
```

###~~初始化数据库~~
~~在mysql中创建一个叫`stuinfo`的数据库，然后执行`./create_table.py localhost`~~  
如需删除所有数据重新创建，执行`./create_table.py localhost --drop`  
如果在docker中执行，把 localhost 替换成 db 即可

###启动测试服务器
运行`./start_debug_server.py`

###生产服务器
现在生产服务器使用docker和docker-compose
具体方法参见[StuInfoSite-Deploy](https://github.com/starsharp06sharp/StuInfoSite-Deploy)