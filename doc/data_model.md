# 数据表定义



## 一、用户管理

### AdminTable

| 列名      | 数据类型及精度 | 约束条件    | 说明                   |
| --------- | -------------- | ----------- | ---------------------- |
| user_name | varchar(20)    | PRIMARY KEY | 账户名是管理员唯一标识 |
| password  | varchar(20)    | NOT NULL    | 管理员密码             |



### UserTable

| 列名               | 数据类型及精度 | 约束条件                            | 说明                                               |
| ------------------ | -------------- | ----------------------------------- | -------------------------------------------------- |
| id                 | varchar(50)    | PRIMARY KEY                         | 微信提供的唯一标识openid                           |
| user_name          | varchar(20)    | NOT NULL                            | 用户名                                             |
| recent_choice_que  | int            | CHECK(>=0)                          | 该用户近期答对选择题的数量                         |
| recent_cloze_que   | int            | CHECK(>=0)                          | 该用户近期答对完形小题的数量                       |
| recent_reading_que | int            | CHECK(>=0)                          | 该用户近期答对阅读小题的数量                       |
| total_choice_que   | int            | CHECK(>=0)                          | 用户做过的选择题的总数                             |
| right_choice_que   | int            | CHECK(>=0)                          | 用户做对的选择题的数量                             |
| total_reading_que  | int            | CHECK(>=0)                          | 用户做过的阅读小题的总数                           |
| right_reading_que  | int            | CHECK(>=0)                          | 用户做对的阅读小题的数量                           |
| total_cloze_que    | int            | CHECK(>=0)                          | 用户做过的完形小题的总数                           |
| right_cloze_que    | int            | CHECK(>=0)                          | 用户做对的完形小题的数量                           |
| status             | int            | NOT NULL, CHECK(type in {"0", "1"}) | 0表示用户正在刷题库中的题，1表示正在刷错题本中的题 |



## 二、题库管理

### Question

| 列名        | 数据类型及精度 | 约束条件                                                     | 说明                             |
| ----------- | -------------- | ------------------------------------------------------------ | -------------------------------- |
| id          | int            | PRIMARY KEY, AUTO_INCREMENT                                  | 题目唯一标识                     |
| titile      | text           | NOT NULL                                                     | 题目的标题                       |
| type        | varchar(20)    | NOT NULL, CHECK(type in {"选择", "阅读", "完形"})            | 题目类型                         |
| text        | text           | CHECK((type='选择' AND text IS NULL) OR text IS NOT NULL)    | 阅读、完形的文章，选择题此项为空 |
| sub_que_num | int            | CHECK((type='选择' AND sub_que_num = 1) OR sub_que_num >=1 ) | 该题目所含小题数量               |



### SubQuestion

| 列名   | 数据类型及精度 | 约束条件                                                     | 说明                   |
| ------ | -------------- | ------------------------------------------------------------ | ---------------------- |
| id     | int            | PRIMARY KEY, AUTO_INCREMENT                                  | 子问题id               |
| que_id | int            | FOREIGN KEY(Question(id))                                    | 子问题所属的父问题的id |
| number | int            | CHECK(number>=1 AND number <= Question(sub_que_num))         | 子问题的题号           |
| stem   | text           | CHECK((Question(id)=father_id AND Question(type)='完形' AND stem IS NULL) OR stem IS NOT NULL) | 题干内容               |
| A      | text           | NOT NULL                                                     | A选项内容              |
| B      | text           | NOT NULL                                                     | B选项内容              |
| C      | text           | NOT NULL                                                     | C选项内容              |
| D      | text           | NOT NULL                                                     | D选项内容              |
| answer | varchar(20)    | NOT NULL, CHECK(answer in {"A", "B", "C", "D"})              | 答案                   |



## 三、刷题功能

### Solution

| 列名         | 数据类型及精度 | 约束条件                     | 说明                                         |
| ------------ | -------------- | ---------------------------- | -------------------------------------------- |
| id           | int            | PRIMARY KEY, AUTO_INCREMENT  | 题解id                                       |
| que_id       | int            | FOREIGN KEY(SubQuestion(id)) | 题解对应小题的id                             |
| content      | text           | NOT NULL                     | 题解内容                                     |
| likes        | int            | CHECK(>=0)                   | 该题解被点赞次数                             |
| reports      | int            | CHECK(>=0)                   | 该题解被举报次数                             |
| bad_solution | bool           |                              | 该题解是否因被举报比例过大，而需被管理员检查 |



### QuestionExclude

| 列名    | 数据类型及精度 | 约束条件                                | 说明   |
| ------- | -------------- | --------------------------------------- | ------ |
| user_id | varchar(30)    | FOREIGN KEY(UserTable(id)), PRIMARY KEY | 用户id |
| que_id  | int            | FOREIGN KEY(Question(id)), PRIMARY KEY  | 题目id |



## 四、用户成绩分析功能

### Record

| 列名    | 数据类型及精度 | 约束条件                                  | 说明                       |
| ------- | -------------- | ----------------------------------------- | -------------------------- |
| date    | datetime       | PRIMARY KEY                               | 用户完成该题目的日期时间   |
| user_id | varchar(30)    | FOREIGN KEY(UserTable(id)),   PRIMARY KEY | 该条刷题记录所属用户的id   |
| que_id  | int            | FOREIGN KEY(Question(id))                 | 该条刷题记录所对应题目的id |



### WrongQuestionBook

| 列名      | 数据类型及精度 | 约束条件                                                     | 说明                       |
| --------- | -------------- | ------------------------------------------------------------ | -------------------------- |
| user_id   | varchar(30)    | FOREIGN KEY(UserTable(id)), PRIMARY KEY                      | 该条错题记录所属用户的id   |
| que_id    | int            | FOREIGN KEY(Question(id)), PRIMARY KEY                       | 该条错题记录所对应题目的id |
| date      | datetime       | NOT NULL                                                     | 用户完成该题的日期         |
| right_num | int            | CHECK(Question(id)=que_id AND right_num >=0 AND right_num <= Question(num)) | 用户答对该题的小题数       |



### UserAnswer

| 列名        | 数据类型及精度 | 约束条件                                        | 说明                             |
| ----------- | -------------- | ----------------------------------------------- | -------------------------------- |
| sub_que_id  | int            | FOREIGN KEY(SubQuestion(id)),  PRIMARY KEY      | 小题的id                         |
| user_id     | varchar(30)    | FOREIGN KEY(UserTable(id)),  PRIMARY KEY        | 用户的id                         |
| user_answer | varchar(20)    | NOT NULL, CHECK(answer in {"A", "B", "C", "D"}) | 用户最后一次作答此题时提交的答案 |



### Notice

| 列名    | 数据类型及精度 | 约束条件                    | 说明         |
| ------- | -------------- | --------------------------- | ------------ |
| id      | int            | PRIMARY KEY, AUTO_INCREMENT | 此条公告的id |
| contant | text           | NOT NULL                    | 公告内容     |
| date    | datetime       | NOT NULL                    | 公告创建时间 |

