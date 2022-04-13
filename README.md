##  Newbee English



#### Backend 小组仓库

本小组仓库：[SnapdragonLee/Newbee-backend (github.com)](https://github.com/SnapdragonLee/Newbee-backend)

主仓库: [SnapdragonLee/Newbee-English (github.com)](https://github.com/SnapdragonLee/Newbee-English)



#### Backend 环境配置

使用 **Django 3.2 LTS**，而非最新版本 4.0。



*其余请使用如下命令，以获得相关包：

`python -m pip install -r requirements.txt` 



#### Backend 小组成员

李霄龙 姜田龙 张昊雨



#### 使用django自带的管理平台修改数据库数据

首先需建立超级账户，账户名密码自行设置，邮箱可为空

```
python manage.py createsuperuser
Username (leave blank to use 'root'): admin
Email address: 
Password:
Password (again):
Superuser created successfully.
```



在浏览器中输入http://127.0.0.1:8000/DJadmin ，用刚才注册的超级用户登录，即可进入管理界面



为了让 admin 界面管理某个数据模型，我们需要先注册该数据模型到 admin。比如，client这个app中的WXUser模型。如下修改 client/admin.py，即可在管理页面修改该模型在数据库中的内容

```python
from django.contrib import admin
from .models import WXUser

# Register your models here.

admin.site.register(WXUser)
```



#### 使用DRF框架的管理平台

比如，管理员登录的这个视图：

```python
@api_view(['POST'])
def admin_login(request):
    username = request.data['name']
    password = request.data['pwd']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return drf_response(0)
    else:
        return drf_response(1)
```

此视图对应的路由是/admin/login/，在浏览器中访问 http://127.0.0.1:8000/admin/login/   ，即可模拟前端向后端发送json，点击post按键，可查看后端返回给前端的json