# 数据表定义



## 一、用户管理



##### AdminTable

| 列名      | 数据类型及精度 | 约束条件    | 说明                   | 备注 |
| --------- | -------------- | ----------- | ---------------------- | ---- |
| user_name | varchar(20)    | PRIMARY KEY | 账户名是管理员唯一标识 |      |
| password  | varchar(20)    | NOT NULL    | 管理员密码             |      |



##### UserTable

| 列名             | 数据类型及精度 | 约束条件                    | 说明                   | 备注 |
| ---------------- | -------------- | --------------------------- | ---------------------- | ---- |
| id               | int            | PRIMARY KEY, AUTO_INCREMENT | 用户唯一标识           |      |
| user_name        | varchar(20)    | UNIQUE, NOT NULL            | 用户名                 |      |
| image            | varchar(100)   | NOT NULL                    | 用户头像               |      |
| notebook         | int            | FOREIGN KEY                 | 用户错题本的id         |      |
| record           | int            | FOREIGN KEY                 | 用户刷题记录的id       |      |
| analysis         | int            | FOREIGN KEY                 | 用户刷题分析的id       |      |
| reading_ques_cnt | int            | CHECK(>=0)                  | 近期阅读题做对的小题数 |      |
| cloze_ques_cnt   | int            | CHECK(>=0)                  | 近期完形做对的小题数   |      |
| choice_ques_cnt  | int            | CHECK(>=0)                  | 近期选择题做对的题数   |      |