## Develop Guide



#### 使用 django 自带的管理平台修改数据库数据

首先需建立超级账户，账户名密码自行设置，邮箱可为空：

```bash
$ python manage.py createsuperuser
Username (leave blank to use 'root'): admin
Email address: 
Password:
Password (again):
Superuser created successfully.
```



在浏览器中输入http://127.0.0.1:8000/DJadmin/ ，用刚才注册的超级用户登录，即可进入管理界面。



为了让 admin 界面管理某个数据模型，我们需要先注册该数据模型到 admin。比如，client 这个 app 中的WXUser 模型。如下修改 client/admin.py：

```python
from django.contrib import admin
from .models import WXUser

# Register your models here.

admin.site.register(WXUser)
```



即可在管理页面修改该模型在数据库中的内容。
