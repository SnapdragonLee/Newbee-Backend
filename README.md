##  Newbee Backend



### Description

各个小组代码仓库：

| 小组                | 仓库地址                                                     |
| ------------------- | ------------------------------------------------------------ |
| Main                | [SnapdragonLee/Newbee-English (github.com)](https://github.com/SnapdragonLee/Newbee-English) |
| Backend             | [SnapdragonLee/Newbee-backend (github.com)](https://github.com/SnapdragonLee/Newbee-backend) |
| Frontend            | [zrjzrj0403/Newbee-Frontend (github.com)](https://github.com/zrjzrj0403/Newbee-Frontend) |
| Weixin Mini Program | [edwardyangjh/miniprogram_Newbee English (gitee.com)](https://gitee.com/edwardyangjh/newbee-english) |



### Backend 环境配置

使用 **Django 3.2 LTS**，而非最新版本 4.0。



*其余请使用如下命令，以获得相关包：

```bash
python -m pip install -r requirements.txt 
```



详细文档请查看文件 `Develop Guide.md` 。



### Backend 搭配 vue 前端静态显示

在 vue 前端目录 `frontend/` 运行指令：

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



**千万不要擅自改动 `backend/src/mysite/mysite/settings.py` 中的配置！改之前最好问下后端的各个组员，或者让他们内部商量一下。**



*你也可以根据自己的 OS 和环境，通过使用主仓库中的 `autoLayout.sh`，`autoLayout.bat`，`autoLayout.ps1` 全自动准备联调环境。*



### Backend 小组成员

李霄龙 姜田龙 张昊雨