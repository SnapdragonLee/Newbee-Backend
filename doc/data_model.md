# 数据表定义



## 一、用户管理

### AdminTable

| 列名      | 数据类型及精度 | 约束条件    | 说明                   |
| --------- | -------------- | ----------- | ---------------------- |
| user_name | varchar(20)    | PRIMARY KEY | 账户名是管理员唯一标识 |
| password  | varchar(20)    | NOT NULL    | 管理员密码             |



### UserTable

| 列名      | 数据类型及精度 | 约束条件                    | 说明               |
| --------- | -------------- | --------------------------- | ------------------ |
| id        | int            | PRIMARY KEY, AUTO_INCREMENT | 用户唯一标识       |
| openid    | varchar(30)    | PRIMARY KEY                 | 微信提供的唯一标识 |
| user_name | varchar(20)    | UNIQUE, NOT NULL            | 用户名             |
| image     | varchar(100)   | NOT NULL                    | 用户头像           |



## 二、题库管理

### Question

| 列名        | 数据类型及精度 | 约束条件                                                     | 说明                             |
| ----------- | -------------- | ------------------------------------------------------------ | -------------------------------- |
| id          | int            | PRIMARY KEY, AUTO_INCREMENT                                  | 题目唯一标识                     |
| type        | varchar(20)    | NOT NULL, CHECK(type in {"选择", "阅读", "完形"})            | 题目类型                         |
| text        | text           | CHECK((type='选择' AND text IS NULL) OR text IS NOT NULL)    | 阅读、完形的文章，选择题此项为空 |
| sub_que_num | int            | CHECK((type='选择' AND sub_que_num = 1) OR sub_que_num >=1 ) | 该题目所含小题数量               |



### SubQuestion

| 列名   | 数据类型及精度 | 约束条件                                                     | 说明                   |
| ------ | -------------- | ------------------------------------------------------------ | ---------------------- |
| id     | int            | PRIMARY KEY, AUTO_INCREMENT                                  | 子问题id               |
| que_id | int            | FOREIGN KEY(Question(id))                                    | 子问题所属的父问题的id |
| stem   | text           | CHECK((Question(id)=father_id AND Question(type)='完形' AND stem IS NULL) OR stem IS NOT NULL) | 题干内容               |
| A      | text           | NOT NULL                                                     | A选项内容              |
| B      | text           | NOT NULL                                                     | B选项内容              |
| C      | text           | NOT NULL                                                     | C选项内容              |
| D      | text           | NOT NULL                                                     | D选项内容              |
| answer | varchar(20)    | NOT NULL, CHECK(answer in {"A", "B", "C", "D"})              | 答案                   |



## 三、刷题功能

### Solution

| 列名    | 数据类型及精度 | 约束条件                     | 说明             |
| ------- | -------------- | ---------------------------- | ---------------- |
| id      | int            | PRIMARY KEY, AUTO_INCREMENT  | 题解id           |
| que_id  | int            | FOREIGN KEY(SubQuestion(id)) | 题解对应小题的id |
| content | text           | NOT NULL                     | 题解内容         |
| likes   | int            | CHECK(>=0)                   | 该题解被点赞次数 |
| report  | int            | CHECK(>=0)                   | 该题解被举报次数 |



## 四、用户成绩分析功能

### Record

| 列名    | 数据类型及精度 | 约束条件                    | 说明                       |
| ------- | -------------- | --------------------------- | -------------------------- |
| id      | int            | PRIMARY KEY, AUTO_INCREMENT | 该条刷题记录的id           |
| user_id | int            | FOREIGN KEY(UserTable(id))  | 该条刷题记录所属用户的id   |
| que_id  | int            | FOREIGN KEY(Question(id))   | 该条刷题记录所对应题目的id |
| date    | datatime       | NOT NULL                    | 用户完成该题目的时间       |



### WrongQuestionBook

| 列名      | 数据类型及精度 | 约束条件                                                     | 说明                       |
| --------- | -------------- | ------------------------------------------------------------ | -------------------------- |
| id        | int            | PRIMARY KEY, AUTO_INCREMENT                                  | 该错题记录的id             |
| user_id   | int            | FOREIGN KEY(UserTable(id))                                   | 该条错题记录所属用户的id   |
| que_id    | int            | FOREIGN KEY(Question(id))                                    | 该条错题记录所对应题目的id |
| date      | datatime       | NOT NULL                                                     | 用户完成该题目的时间       |
| right_num | int            | CHECK(Question(id)=que_id AND right_num >=0 AND right_num <= Question(num)) | 用户答对该题的小题数       |



### Statistic

| 列名              | 数据类型及精度 | 约束条件                    | 说明                     |
| ----------------- | -------------- | --------------------------- | ------------------------ |
| id                | int            | PRIMARY KEY, AUTO_INCREMENT | 该条统计的id             |
| user_id           | int            | FOREIGN KEY(UserTable(id))  | 该条统计所属的用户id     |
| choice_que_total  | int            | CHECK(>=0)                  | 用户做过的选择题的总数   |
| choice_que_right  | int            | CHECK(>=0)                  | 用户做对的选择题的数量   |
| reading_que_total | int            | CHECK(>=0)                  | 用户做过的阅读小题的总数 |
| reading_que_right | int            | CHECK(>=0)                  | 用户做对的阅读小题的数量 |
| cloze_que_total   | int            | CHECK(>=0)                  | 用户做过的完形小题的总数 |
| cloze_que_right   | int            | CHECK(>=0)                  | 用户做对的完形小题的数量 |



### Rank

| 列名        | 数据类型及精度 | 约束条件                    | 说明                         |
| ----------- | -------------- | --------------------------- | ---------------------------- |
| id          | int            | PRIMARY KEY, AUTO_INCREMENT | 该条排行的id                 |
| user_id     | int            | FOREIGN KEY(UserTable(id))  | 该条排行所属的用户id         |
| choice_que  | int            | CHECK(>=0)                  | 该用户近期答对选择题的数量   |
| cloze_que   | int            | CHECK(>=0)                  | 该用户近期答对完形小题的数量 |
| reading_que | int            | CHECK(>=0)                  | 该用户近期答对阅读小题的数量 |
