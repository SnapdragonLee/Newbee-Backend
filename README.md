##  Newbee English



### Backend 小组仓库

本小组仓库：[SnapdragonLee/Newbee-backend (github.com)](https://github.com/SnapdragonLee/Newbee-backend)

主仓库: [SnapdragonLee/Newbee-English (github.com)](https://github.com/SnapdragonLee/Newbee-English)



### Backend 环境配置

使用 **Django 3.2 LTS**，而非最新版本 4.0。



*其余请使用如下命令，以获得相关包：

```bash
python -m pip install -r requirements.txt 
```



详细文档请查看文件 `Develop Guide.md` 。



### Backend 搭配 vue 前端静态显示

在 vue 前端运行指令：

```bash
npm install
npm run build
```



之后将 `frontend/` 下的 `dist` 目录拷贝至 `backend/src/mysite/` 下。

此时，直接启动 Django 后端，即可看到前端的静态页面：

```bash
cd src/mysite/
python manage.py runserver 8000
```



**千万不要擅自改动 `backend/src/mysite/mysite/settings.py` 中的配置！不要问我为什么！**

**千万不要擅自改动 `backend/src/mysite/mysite/settings.py` 中的配置！不要问我为什么！**



### Backend 小组成员

李霄龙 姜田龙 张昊雨