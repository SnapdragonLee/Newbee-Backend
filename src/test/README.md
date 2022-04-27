## Backend API 测试脚本说明



### 使用方法

先使用角色登录进入系统，选择测试脚本名称 (位于对应角色 `profile/` 目录下)，选择测试地址 (可选服务器、本地测试)，具体需要填写的项目见本目录下的 `test.py` 。

```python
test_actor = "admin"  # something like "admin" \ "client"
test_profile = "admin_logout"  # you need to create json file in profile documents


main_addr = "http://127.0.0.1:8000"  # local server location
# main_addr = "http://122.9.32.180"  # remote server location
```

例如，使用 admin 登录系统，需要测试的 API 名称为 `getname`，则 `test_actor = "admin"`，`test_profile = "admin_getname"` **（这两个项对应脚本的目录位置）**。

注意，你需要确保 `admin/profile/admin_getname.json` 文件存在，且根据不同的 API，该文件的 `data` 项 **需要（或不需要）** 填入数据。

每一次测试的时候，只需要更改对应的 json 文件下的 data，以及 `test.py` 文件中的脚本路径即可，测试的时候只需要直接运行 `test.py` 即可。



### 原理

这个部分不想说太多，主要是首先调用测试对应的 `.json` 文件中的 `login_data` 项进行登录，然后保持 Session 的情况下再使用配置中的 `test_api` 项找到对应测试服务器的 API 位置，之后将 data 项通过打包 json 数据格式发送给 session 会话，并自动根据类别 `GET/DELETE/PATCH/PUT/POST` 等进行判断，并根据后端返回的 debug 信息进行 json 录入，直接将有用的信息返回。



### 优势

不需要 Postman 等软件，只需要简单的 Python 环境，以及更改一些语句、填入 data 即可进行测试。测试的脚本所有人共享，不需要每个人自己创造数据，对于每一个错误样例，都可以创建对应的 json 测试文件。

