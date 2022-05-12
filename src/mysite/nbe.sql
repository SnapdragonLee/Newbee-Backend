/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 80027
 Source Host           : localhost:3306
 Source Schema         : nbe

 Target Server Type    : MySQL
 Target Server Version : 80027
 File Encoding         : 65001

 Date: 12/05/2022 10:55:04
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for administrator_adminapprovesolution
-- ----------------------------
DROP TABLE IF EXISTS `administrator_adminapprovesolution`;
CREATE TABLE `administrator_adminapprovesolution`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `admin_id` int NOT NULL,
  `solution_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `administrator_admina_admin_id_bf1e7a24_fk_auth_user`(`admin_id` ASC) USING BTREE,
  INDEX `administrator_admina_solution_id_78c92f14_fk_administr`(`solution_id` ASC) USING BTREE,
  CONSTRAINT `administrator_admina_admin_id_bf1e7a24_fk_auth_user` FOREIGN KEY (`admin_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `administrator_admina_solution_id_78c92f14_fk_administr` FOREIGN KEY (`solution_id`) REFERENCES `administrator_solution` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of administrator_adminapprovesolution
-- ----------------------------

-- ----------------------------
-- Table structure for administrator_notice
-- ----------------------------
DROP TABLE IF EXISTS `administrator_notice`;
CREATE TABLE `administrator_notice`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `time` datetime(6) NOT NULL,
  `content` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of administrator_notice
-- ----------------------------
INSERT INTO `administrator_notice` VALUES (1, '2022-05-11 13:51:58.437629', '可能出现的问题就是 没有在登录之后刷新小程序状态');

-- ----------------------------
-- Table structure for administrator_operationrecord
-- ----------------------------
DROP TABLE IF EXISTS `administrator_operationrecord`;
CREATE TABLE `administrator_operationrecord`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `operation` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `time` datetime(6) NOT NULL,
  `admin_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `administrator_operationrecord_admin_id_40277730_fk_auth_user_id`(`admin_id` ASC) USING BTREE,
  CONSTRAINT `administrator_operationrecord_admin_id_40277730_fk_auth_user_id` FOREIGN KEY (`admin_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of administrator_operationrecord
-- ----------------------------
INSERT INTO `administrator_operationrecord` VALUES (1, '添加', '123123', '2022-05-08 09:29:54.380625', 1);
INSERT INTO `administrator_operationrecord` VALUES (2, '添加', '2019西城一模选择题1', '2022-05-08 09:30:43.166110', 1);
INSERT INTO `administrator_operationrecord` VALUES (3, '删除', '2019西城一模选择题1', '2022-05-08 09:42:13.775657', 1);
INSERT INTO `administrator_operationrecord` VALUES (4, '删除', '123123', '2022-05-08 09:42:19.313635', 1);
INSERT INTO `administrator_operationrecord` VALUES (5, '添加', '2020年西城区英语一模选择1', '2022-05-08 09:48:00.033694', 1);
INSERT INTO `administrator_operationrecord` VALUES (6, '添加', '2020年西城区英语一模选择2', '2022-05-08 09:49:36.826778', 1);
INSERT INTO `administrator_operationrecord` VALUES (7, '添加', 'werthjk.', '2022-05-08 09:50:20.601898', 1);
INSERT INTO `administrator_operationrecord` VALUES (8, '修改', '2020年西城区英语一模选择2', '2022-05-08 09:50:23.580210', 1);
INSERT INTO `administrator_operationrecord` VALUES (9, '删除', 'werthjk.', '2022-05-08 09:51:04.223322', 1);
INSERT INTO `administrator_operationrecord` VALUES (10, '添加', '1. Peter, why didn’t you go to the flower show?', '2022-05-08 09:55:36.337851', 1);
INSERT INTO `administrator_operationrecord` VALUES (11, '添加', '2. The rainy season is coming and let’s make full use of the ______ days to\n\ndry whatever is needed to dry before the next dry season.', '2022-05-08 09:56:08.849664', 1);
INSERT INTO `administrator_operationrecord` VALUES (12, '添加', '3. Americans eat ______ as they actually need every day.', '2022-05-08 09:56:39.831339', 1);
INSERT INTO `administrator_operationrecord` VALUES (13, '添加', 'Goods imported from abroad are', '2022-05-08 09:57:34.020308', 1);
INSERT INTO `administrator_operationrecord` VALUES (14, '添加', 'He was lying in hospital ______, with his ribs broken.', '2022-05-08 09:57:53.370282', 1);
INSERT INTO `administrator_operationrecord` VALUES (15, '添加', 'Are you satisfied with his work, sir?\n\n--- Well, I’m afraid it couldn’t be', '2022-05-08 09:58:50.323781', 1);
INSERT INTO `administrator_operationrecord` VALUES (16, '添加', 'Tom is very stupid. ', '2022-05-08 09:59:11.782732', 1);
INSERT INTO `administrator_operationrecord` VALUES (17, '添加', 'She is always ready to help people in trouble because she thinks it\n\n_____.', '2022-05-08 09:59:34.528180', 1);
INSERT INTO `administrator_operationrecord` VALUES (18, '添加', 'Some trees are cut down each year and ______ are left to grow even taller.\n\nA. the rest', '2022-05-08 09:59:52.957565', 1);
INSERT INTO `administrator_operationrecord` VALUES (19, '添加', 'I don’t like this pair of gloves. Will you show me_____?', '2022-05-08 10:00:10.903227', 1);
INSERT INTO `administrator_operationrecord` VALUES (20, '添加', 'This pair of trousers ______ for John.', '2022-05-08 10:00:31.935344', 1);
INSERT INTO `administrator_operationrecord` VALUES (21, '添加', ' As a result of the heavy snow, the highway has been closed up until further\n\n______.', '2022-05-08 10:00:45.104643', 1);
INSERT INTO `administrator_operationrecord` VALUES (22, '添加', ' --- Could you mail these letters for me please?\n\n ________ letters? Your friends are going to be very happy to hear from', '2022-05-08 10:01:26.137750', 1);
INSERT INTO `administrator_operationrecord` VALUES (23, '添加', 'With summer coming on, the weather gets hot ______.', '2022-05-08 10:02:29.701553', 1);
INSERT INTO `administrator_operationrecord` VALUES (24, '添加', '______ of Guilin has your uncle covered since he came here?\n\n--- About half of it, I guess.', '2022-05-08 10:02:55.372654', 1);
INSERT INTO `administrator_operationrecord` VALUES (25, '添加', 'Two American scientists told the people', '2022-05-08 10:38:52.280442', 1);
INSERT INTO `administrator_operationrecord` VALUES (26, '添加', 'For any Englishman', '2022-05-08 10:53:16.648289', 1);
INSERT INTO `administrator_operationrecord` VALUES (27, '添加', 'Now and again I have had horrible dreams, ', '2022-05-08 11:05:35.393916', 1);
INSERT INTO `administrator_operationrecord` VALUES (28, '添加', 'The day after news broke of a possible revolution in physics', '2022-05-08 11:26:00.590551', 1);
INSERT INTO `administrator_operationrecord` VALUES (29, '修改', ' Americans eat ______ as they actually need every day.', '2022-05-08 11:26:18.574874', 1);
INSERT INTO `administrator_operationrecord` VALUES (30, '修改', 'Peter, why didn’t you go to the flower show?', '2022-05-08 11:26:26.998757', 1);
INSERT INTO `administrator_operationrecord` VALUES (31, '修改', ' The rainy season is coming and let’s make full use of the ______ days to\n\ndry whatever is needed to dry before the next dry season.', '2022-05-08 11:26:33.672905', 1);
INSERT INTO `administrator_operationrecord` VALUES (32, '添加', '测试一下题目长度的问题所以变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长', '2022-05-08 11:57:18.295399', 1);
INSERT INTO `administrator_operationrecord` VALUES (33, '添加', 'When most of us get a text message on our cell phone from an unknown person,', '2022-05-08 12:14:27.311954', 1);
INSERT INTO `administrator_operationrecord` VALUES (34, '修改', 'Some trees are cut down each year and ______ are left to grow even taller.\n\n', '2022-05-08 15:56:42.828554', 1);
INSERT INTO `administrator_operationrecord` VALUES (35, '修改', '公告', '2022-05-10 11:29:46.323542', 1);
INSERT INTO `administrator_operationrecord` VALUES (36, '修改', '公告', '2022-05-10 11:38:39.202585', 1);
INSERT INTO `administrator_operationrecord` VALUES (37, '修改', '公告', '2022-05-10 11:39:04.443620', 1);
INSERT INTO `administrator_operationrecord` VALUES (38, '修改', '公告', '2022-05-10 11:39:09.702155', 1);
INSERT INTO `administrator_operationrecord` VALUES (39, '修改', '公告', '2022-05-10 11:39:18.568435', 1);
INSERT INTO `administrator_operationrecord` VALUES (40, '修改', '公告', '2022-05-10 11:40:14.299267', 1);
INSERT INTO `administrator_operationrecord` VALUES (41, '删除', 'delete_debug', '2022-05-10 11:56:02.620766', 1);
INSERT INTO `administrator_operationrecord` VALUES (42, '删除', 'add_debug', '2022-05-10 11:56:04.708658', 1);
INSERT INTO `administrator_operationrecord` VALUES (43, '添加', 'asdasdasd', '2022-05-10 12:04:28.720993', 1);
INSERT INTO `administrator_operationrecord` VALUES (44, '添加', '1', '2022-05-10 12:04:31.742246', 1);
INSERT INTO `administrator_operationrecord` VALUES (45, '修改', '公告', '2022-05-10 12:05:08.114999', 1);
INSERT INTO `administrator_operationrecord` VALUES (46, '修改', '公告', '2022-05-10 13:40:17.330269', 1);
INSERT INTO `administrator_operationrecord` VALUES (47, '修改', '公告', '2022-05-10 15:00:49.842998', 1);
INSERT INTO `administrator_operationrecord` VALUES (48, '修改', '公告', '2022-05-10 15:04:49.926081', 1);
INSERT INTO `administrator_operationrecord` VALUES (49, '修改', '公告', '2022-05-10 16:02:26.685819', 1);
INSERT INTO `administrator_operationrecord` VALUES (50, '修改', '公告', '2022-05-10 16:19:07.377959', 1);
INSERT INTO `administrator_operationrecord` VALUES (51, '修改', '公告', '2022-05-10 16:19:37.180305', 1);
INSERT INTO `administrator_operationrecord` VALUES (52, '删除', '小程序用户: 圍棋少年李霄龍', '2022-05-11 06:45:33.924226', 1);
INSERT INTO `administrator_operationrecord` VALUES (53, '删除', '1', '2022-05-11 11:30:21.625668', 1);
INSERT INTO `administrator_operationrecord` VALUES (54, '修改', '公告', '2022-05-11 12:15:02.281712', 1);
INSERT INTO `administrator_operationrecord` VALUES (55, '修改', '公告', '2022-05-11 13:51:58.444344', 1);
INSERT INTO `administrator_operationrecord` VALUES (56, '修改', 'I don’t like this pair of gloves. Will you show me_____?', '2022-05-11 20:38:16.177582', 1);

-- ----------------------------
-- Table structure for administrator_question
-- ----------------------------
DROP TABLE IF EXISTS `administrator_question`;
CREATE TABLE `administrator_question`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `type` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `text` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `sub_que_num` int NOT NULL,
  `bad_solution_num` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  CONSTRAINT `check_Question_bad_solution_num` CHECK (`bad_solution_num` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of administrator_question
-- ----------------------------
INSERT INTO `administrator_question` VALUES (3, '2020年西城区英语一模选择1', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (4, '2020年西城区英语一模选择2', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (6, 'Peter, why didn’t you go to the flower show?', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (7, ' The rainy season is coming and let’s make full use of the ______ days to\n\ndry whatever is needed to dry before the next dry season.', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (8, ' Americans eat ______ as they actually need every day.', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (9, 'Goods imported from abroad are', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (10, 'He was lying in hospital ______, with his ribs broken.', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (11, 'Are you satisfied with his work, sir?\n\n--- Well, I’m afraid it couldn’t be', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (12, 'Tom is very stupid. ', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (13, 'She is always ready to help people in trouble because she thinks it\n\n_____.', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (14, 'Some trees are cut down each year and ______ are left to grow even taller.\n\n', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (15, 'I don’t like this pair of gloves. Will you show me_____?', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (16, 'This pair of trousers ______ for John.', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (17, ' As a result of the heavy snow, the highway has been closed up until further\n\n______.', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (18, ' --- Could you mail these letters for me please?\n\n ________ letters? Your friends are going to be very happy to hear from', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (19, 'With summer coming on, the weather gets hot ______.', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (20, '______ of Guilin has your uncle covered since he came here?\n\n--- About half of it, I guess.', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (21, 'Two American scientists told the people', 'reading_question', 'Two American scientists told the people in industrial nations that they would be much healthier if they ate more of the same kind of foods eaten by humans living more than 10,000 years ago．\n\nThe scientists say that the human body has changed very little since human first appeared on earth, but the way we live has changed greatly．Our body has not been able to deal with these changes in life style and this has led to new kinds of sicknesses．These new sicknesses were not known1 in ancient times．So they are called “diseases2 of civilization（文明）”．Many cancers（癌） and diseases of the blood system, including heart attacks and strokes3（中风） are examples of such diseases．\n\nScientists noted4 that early stone-age people used very little alcohol5（酒精）or tabacco, probably none．Ancient people also got a great deal of physical exercise, but a change in food is one of the main differences between life in ancient times and life today．\n\nStone-age people hunted wild animals for their meat, which had much less fat than farm animals．They also ate a lot of fresh wild vegetables, and fruits．They did not use milk and other dairy6 products（乳制品）, and they made very little use of grains．But today, we eat a large amount of dairy products and grain foods．We eat six times more salt than stone-age people．We eat more sugar．We eat twice as much fat but only one third as much protein（蛋白质）and much less vitamin7（维生素）C．\n\nPeople today probably do not want to live as people thousands of years ago did, but scientists say that we would be much healthier if we ate as those ancient people did, cutting the amount of fatty, salty and sweet foods．', 5, 0);
INSERT INTO `administrator_question` VALUES (22, 'For any Englishman', 'reading_question', '　For any Englishman，there can never be any discussion as to who is the worlds greatest dramatist(剧作家).Only one name can possibly suggest itself to him：that of William Shakespeare Every Englishman has some knowledge，however slight，of the work of our greatest writer.All of US use words，phrases and quotations from Shakespeares writings that have become part of the common property of the English-speaking people.Most of the time we are probably unaware of the source of the words we used，rather like the old lady who was taken to see a performance of Hamlet and complained that it was full of well—known proverbs and quotations.\n　　Shakespeare，more perhaps than any other writer，makes full use of the great resources of the English language.Most of US use about five thousand words in our normal use of English;Shakespeare in his works used about twenty-five thousand.\n　　There is probably no better way for a foreigner to appreciate the richness and variety of the English language than by studying the various ways in which Shakespeare used it.Such a study is well worth the effort(it is not，of course，recommended to beginners)even though some aspects of English usage，and the meaning of many words，have changed since Shakespeares day.\n', 5, 0);
INSERT INTO `administrator_question` VALUES (23, 'Now and again I have had horrible dreams, ', 'reading_question', 'Now and again I have had horrible dreams, but not enough of them to make me lose my delight in dreams. To begin with. I like the idea of dreaming, of going to bed and lying still and then, by some queer magic(神奇的魔力), wandering into another kind of existence. As a child, I could never understand why grown-ups took dreaming so calmly when they could make such a fuss(大惊小怪) about any holiday, This still puzzles me. I am puzzled by people who say they never dream and appear to have no interest in the subject. It is much more astonishing than it would be if they said they never went out for a walk. Most people do not seem to accept dreaming as part of their lives. They appear to see it as an irritating(令人困扰的) little habit, like sneezing or yawning(打哈欠).I can never understand this. My dream life does not seem as important as my waking life because there is far less of it, but to me it is important.', 4, 0);
INSERT INTO `administrator_question` VALUES (24, 'The day after news broke of a possible revolution in physics', 'reading_question', 'The day after news broke of a possible revolution in physics——particles(粒子)moving faster than light? a scientist leading the European experiment that made the discovery calmly explained it to a standing-room-only crowd at CERN．\n\n　　The physicist, Dario Auterio, did not try to explain what the results might mean for the laws of physics, let alone the broader world．After an hour of technical talk, he simply said, \"Therefore, we present to you today this difference, this unusualness．\"\n\n　　But what unusualness it may be．From 2009 through 2011, the massive OPERA detector(探测器)buried in a mountain in Gran Sasso, Italy, recorded subatomic particles called neutrinos(中微子)arriving faster than light can move in an empty space．The neutrinos generated at CERN are hardly detectably early．If confirmed, the finding would throw more than a century of physics into disorder．\n\n　　\"If it\'s correct, it\'s phenomenal．\" said Rob Plunkett, a scientist at Fermilab, the Department of Energy physics laboratory in Illinois．\"We\'d be looking at a whole new set of rules\" for how the universe works．Those rules would bend, or possibly break, Albert Einstein\'s special theory of relativity, published in 1905．Basical at the time, the theory tied together space and time, matter and energy, and set a hard limit for the speed of light, later measured to be about 186, 000 miles per second．\n\n　　No experiment in 106 years had broken that speed limit．Physicists expect strict study to follow, which OPERA and CERN scientists welcomed．\n\n　　Fermilab operates a similar experiment, called MINOS, that shoots neutrinos from Illinois to an underground detector in Minnesota．In 2007, MINOS discovered a just detectable amount of faster than-light neutrinos, but the permissible difference of error was too big to \"mention\", Plunkett said．\n\n　　Fermilab scientists will reanalyze their data, which will take six to eight months．In 2013, the MINOS detector, now offline, will restart after an upgrade．It could then offer confirmation of the results．', 4, 0);
INSERT INTO `administrator_question` VALUES (25, '测试一下题目长度的问题所以变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长变长', 'choice_question', NULL, 1, 0);
INSERT INTO `administrator_question` VALUES (26, 'When most of us get a text message on our cell phone from an unknown person,', 'cloze_question', 'When most of us get a text message on our cell phone from an unknown person, we usually say ＂sorry, ____41____ number!＂ and move on. But when Dennis Williams _____42_____ a text that clearly wasn’t intended for him, he did something _____43_____.On March 19, Dennis got a group text _____44_____ him that a couple he didn’t know were at the hospital, waiting for the _____45_____ of a baby.＂Congratulations! But I think someone was mistaken,＂ Dennis _____46_____. The baby was born and update texts were _____47_____ quickly from the overjoyed grandmother, Teresa. In her _____48_____, she didn’t seem to realize that she was _____49_____ the baby’s photos with a complete stranger. ＂Well, I don’t _____50_____ you all but I will get there to take pictures with the baby,＂ replied Dennis before asking which room the new parents were in.\n\n \n', 10, 0);
INSERT INTO `administrator_question` VALUES (29, 'asdasdasd', 'choice_question', NULL, 1, 0);

-- ----------------------------
-- Table structure for administrator_solution
-- ----------------------------
DROP TABLE IF EXISTS `administrator_solution`;
CREATE TABLE `administrator_solution`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `likes` int NOT NULL,
  `reports` int NOT NULL,
  `approval` int NOT NULL,
  `is_bad` tinyint(1) NOT NULL,
  `subQuestion_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `administrator_soluti_subQuestion_id_38a889a3_fk_administr`(`subQuestion_id` ASC) USING BTREE,
  CONSTRAINT `administrator_soluti_subQuestion_id_38a889a3_fk_administr` FOREIGN KEY (`subQuestion_id`) REFERENCES `administrator_subquestion` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `check_approval` CHECK (`approval` >= 0),
  CONSTRAINT `check_likes` CHECK (`likes` >= 0),
  CONSTRAINT `check_reports` CHECK (`reports` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of administrator_solution
-- ----------------------------
INSERT INTO `administrator_solution` VALUES (1, 'hello text1', 0, 0, 0, 0, 12);
INSERT INTO `administrator_solution` VALUES (2, 'dfghjk', 0, 0, 0, 0, 35);
INSERT INTO `administrator_solution` VALUES (3, 'test1', 0, 0, 0, 0, 14);
INSERT INTO `administrator_solution` VALUES (4, 'test2', 0, 0, 0, 0, 14);
INSERT INTO `administrator_solution` VALUES (5, 'test3', 0, 0, 0, 0, 14);
INSERT INTO `administrator_solution` VALUES (6, 'gxdhtfjycgh\n', 0, 0, 0, 0, 7);
INSERT INTO `administrator_solution` VALUES (7, '题解test2', 0, 0, 0, 0, 35);
INSERT INTO `administrator_solution` VALUES (8, '题解test3', 0, 0, 0, 0, 35);

-- ----------------------------
-- Table structure for administrator_subquestion
-- ----------------------------
DROP TABLE IF EXISTS `administrator_subquestion`;
CREATE TABLE `administrator_subquestion`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `number` int NOT NULL,
  `stem` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `A` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `B` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `C` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `D` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `bad_solution_num` int NOT NULL,
  `answer` varchar(5) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `question_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `administrator_subque_question_id_574d8170_fk_administr`(`question_id` ASC) USING BTREE,
  CONSTRAINT `administrator_subque_question_id_574d8170_fk_administr` FOREIGN KEY (`question_id`) REFERENCES `administrator_question` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `check_SubQuestion_bad_solution_num` CHECK (`bad_solution_num` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of administrator_subquestion
-- ----------------------------
INSERT INTO `administrator_subquestion` VALUES (3, 1, 'It ’s so nice to hear from her again. _____, we last met more than thirty years ago.', 'What’s more ', 'That ’s to say', 'In other words ', 'Believe it or not', 0, 'D', 3);
INSERT INTO `administrator_subquestion` VALUES (4, 1, 'I really don’t know　whether I can succeed in the final competition, _____ I will try.', 'and ', 'for ', 'but', 'or', 0, 'C', 4);
INSERT INTO `administrator_subquestion` VALUES (6, 1, 'Peter, why didn’t you go to the flower show? \n--- I think it’s something ______ pleasant.', 'far more', 'far less', 'too much', 'much too', 0, 'B', 6);
INSERT INTO `administrator_subquestion` VALUES (7, 1, ' The rainy season is coming and let’s make full use of the ______ days to\n\ndry whatever is needed to dry before the next dry season.', 'few last sunny', 'last few sunny', 'last sunny few', 'sunny last few', 0, 'B', 7);
INSERT INTO `administrator_subquestion` VALUES (8, 1, 'Americans eat ______ as they actually need every day.', 'twice as much protein', 'twice protein as much twice', 'twice protein as much', 'protein as twice much ', 0, 'A', 8);
INSERT INTO `administrator_subquestion` VALUES (9, 1, 'Goods imported from abroad are ______ those made in China.\n\n--- Yes. Some of the goods made in China are of high quality.', 'not always better than', 'always as good as', 'no better than', 'no longer better than ', 0, 'A', 9);
INSERT INTO `administrator_subquestion` VALUES (10, 1, 'He was lying in hospital ______, with his ribs broken.', 'half dead', 'deadly', 'dying', 'died ', 0, 'A', 10);
INSERT INTO `administrator_subquestion` VALUES (11, 1, ' Are you satisfied with his work, sir?\n\n--- Well, I’m afraid it couldn’t be', 'any better', 'the best', 'any worse', 'the worst', 0, 'C', 11);
INSERT INTO `administrator_subquestion` VALUES (12, 1, 'Tom is very stupid. He fails in every exam.\n\n--- In my opinion, he is _____ than stupid.', 'lazier', 'no lazier', 'more lazy', 'lazier rather ', 0, 'C', 12);
INSERT INTO `administrator_subquestion` VALUES (13, 1, 'She is always ready to help people in trouble because she thinks it\n\n_____.', 'pleasure', 'a fun', 'a pride', 'a pleasure', 0, 'D', 13);
INSERT INTO `administrator_subquestion` VALUES (14, 1, 'Some trees are cut down each year and ______ are left to grow even taller.\n\n', 'the rest', 'rest of them', 'a rest', 'a rest of them', 0, 'A', 14);
INSERT INTO `administrator_subquestion` VALUES (15, 1, 'I don’t like this pair of gloves. Will you show me_____?', 'another', 'the others', 'some others', 'other ones ', 0, 'A', 15);
INSERT INTO `administrator_subquestion` VALUES (16, 1, ' This pair of trousers ______ for John.', 'is made', 'are made', 'makes', 'will make', 0, 'A', 16);
INSERT INTO `administrator_subquestion` VALUES (17, 1, ' As a result of the heavy snow, the highway has been closed up until further\n\n______.', 'news', 'information', 'notice', 'message', 0, 'C', 17);
INSERT INTO `administrator_subquestion` VALUES (18, 1, '  Could you mail these letters for me please?\n\n ________ letters? Your friends are going to be very happy to hear from you again.', 'What', 'Some', 'More', 'different', 0, 'C', 18);
INSERT INTO `administrator_subquestion` VALUES (19, 1, 'With summer coming on, the weather gets hot ______.', 'day after day', 'day and night', 'day in and day out', 'day by day ', 0, 'D', 19);
INSERT INTO `administrator_subquestion` VALUES (20, 1, '______ of Guilin has your uncle covered since he came here?\n\n--- About half of it, I guess.', 'How far', 'How much', 'How wide', 'How many ', 0, 'B', 20);
INSERT INTO `administrator_subquestion` VALUES (21, 1, '1.The people in industrial nations would be much healthier if they ate ______．', 'more foods as humans living 10,000 years ago did', 'as humans living 10,000 years ago ate', 'more kinds of food eaten by people living over 10,000 years ago', 'more of the same kinds of foods eaten by people over 10,000 years ago', 0, 'D', 21);
INSERT INTO `administrator_subquestion` VALUES (22, 2, '2.New kinds of sicknesses have been found because ______', 'the human body has changed compared with human first appeared on earth', 'the way we live has changed a little', 'our body can’t deal with the changes in life style', 'the way we live today are proper for the human body', 0, 'C', 21);
INSERT INTO `administrator_subquestion` VALUES (23, 3, '3．What is the main cause mentioned in the article why people suffer from a lot of new sicknesses?', 'Ancient people did a great deal of physical exercise', 'People today have a lot of alcohol', 'People today have more tobacco', 'Food is quite different between life today and life in ancient times', 0, 'D', 21);
INSERT INTO `administrator_subquestion` VALUES (24, 4, '4.Stone-age people were much healthier than people today because they ate a lot of ______．', 'milk and other dairy products', 'grain foods and farm animals', 'salt and sugar', 'wild animals, fresh wild vegetables and fruits', 0, 'D', 21);
INSERT INTO `administrator_subquestion` VALUES (25, 5, '5.From this article, we know that ______ are not good to our health．', 'protein and vitamin C', 'milk and grain foods', 'wild animals, vegetables and fruits', 'a huge amount of fatty, salty and sweet foods', 0, 'D', 21);
INSERT INTO `administrator_subquestion` VALUES (26, 1, 'English people ______', 'have never discussed who is the worlds greatest dramatist.', 'never discuss any issue concerning the worlds greatest dramatist.', 'are sure who is the worlds greatest dramatist.', 'do not care who is the worlds greatest poet and dramatist.', 0, 'C', 22);
INSERT INTO `administrator_subquestion` VALUES (27, 2, 'Every Englishman knows ______', 'more or less about Shakespeare.', 'Shakespeare,but only slightly.', 'all Shakespeares writings.', 'only the name of the greatest English writer.', 0, 'A', 22);
INSERT INTO `administrator_subquestion` VALUES (28, 3, 'Which of the following is true?', 'We use all the words,phrases and quotations from ShakespeareS writings.', 'Shakespeares writings have become the property of those who are learning to speak English.', 'It is likely to be true that people often do not know the origins of the words they use.', 'All the words people use are taken from the writings of Shakespeare.', 0, 'C', 22);
INSERT INTO `administrator_subquestion` VALUES (29, 4, 'What does the word “proverb” mean?', 'Familiar sayings.', 'Shakespeares plays.', 'Complaints.', 'Actors and actresses.', 0, 'A', 22);
INSERT INTO `administrator_subquestion` VALUES (30, 5, 'Why is it worthwhile to study the various ways in which Shakespeare used English?', 'English words have changed a lot since Shakespeare’S time.', 'By doing SO one can be fully aware of the richness of the English language.', 'English words are now being used in the same way as in Shakespeares time.', 'Beginners may have difficulty learning some aspects of English usage.', 0, 'B', 22);
INSERT INTO `administrator_subquestion` VALUES (31, 1, 'What is the author’s attitude toward dreaming?', 'He thinks it puzzling', 'He likes it', 'He is interested in it', 'He doesn’t accept it as part of his life', 0, 'B', 23);
INSERT INTO `administrator_subquestion` VALUES (32, 2, 'For the author of the passage, dreaming is________.    ', 'another kind of existence', 'an irritating little habit', 'a horrible but wonderful experience', 'a true reflection of reality', 0, 'A', 23);
INSERT INTO `administrator_subquestion` VALUES (33, 3, 'The author of the passage suggests that people who say they never go out for a walk are_____.', 'interesting', 'unbelievable', 'mysterious', 'lazy', 0, 'C', 23);
INSERT INTO `administrator_subquestion` VALUES (34, 4, 'Why does the author of the passage complain?', 'Because most people are overexcited about their dreams', 'Because most people are not interested in talking about their dreams', 'Because most people have had dreams most of the time', 'Because most people consider their dreams of too much importance', 0, 'B', 23);
INSERT INTO `administrator_subquestion` VALUES (35, 1, '	\nWhy are the European scientists not sure about the results of the experiment?', 'Because they are so unexpected', 'Because the scientists do not believe them', 'Because the scientists are careful and calm', 'Because they are against the present law of physics', 0, 'D', 24);
INSERT INTO `administrator_subquestion` VALUES (36, 2, '	\nThe underlined word \" phenomenal\" in the fourth paragraph has the closest meaning to ________．', 'amazing', 'attractive', 'embarrassing', 'sensitive', 0, 'A', 24);
INSERT INTO `administrator_subquestion` VALUES (37, 3, 'The best title for the passage may be ________．', 'Are the laws of physics in disorder?', 'Particles faster than light Revolution or mistake?', 'Faster than light measurement right or wrong?', 'Is Einstein’s theory still right today?', 0, 'B', 24);
INSERT INTO `administrator_subquestion` VALUES (38, 4, 'What may be discussed in the paragraphs to follow?', 'Different opinions about the experiment', 'How Albert Einstein\'s theory developed', 'The new rules for how the universe works', 'How Fermilab scientists will reanalyze their data', 0, 'D', 24);
INSERT INTO `administrator_subquestion` VALUES (39, 1, '123', '1', '2', '3', '4', 0, 'C', 25);
INSERT INTO `administrator_subquestion` VALUES (40, 1, NULL, 'unlucky ', 'secret ', 'new ', 'wrong', 0, 'D', 26);
INSERT INTO `administrator_subquestion` VALUES (41, 2, NULL, 'received ', 'translated ', 'copied ', 'printed', 0, 'A', 26);
INSERT INTO `administrator_subquestion` VALUES (42, 3, NULL, 'reasonable ', 'special ', 'necessary ', 'practical', 0, 'B', 26);
INSERT INTO `administrator_subquestion` VALUES (43, 4, NULL, 'convincing ', 'reminding ', 'informing ', 'warning', 0, 'C', 26);
INSERT INTO `administrator_subquestion` VALUES (44, 5, NULL, 'wake-up ', 'recovery ', 'growth ', 'arrival', 0, 'D', 26);
INSERT INTO `administrator_subquestion` VALUES (45, 6, NULL, 'responded ', 'interrupted ', 'predicted ', 'repeated', 0, 'A', 26);
INSERT INTO `administrator_subquestion` VALUES (46, 7, NULL, 'coming in ', 'setting out ', 'passing down ', 'moving around', 0, 'A', 26);
INSERT INTO `administrator_subquestion` VALUES (47, 8, NULL, 'opinion ', 'anxiety ', 'excitement ', 'effort', 0, 'C', 26);
INSERT INTO `administrator_subquestion` VALUES (48, 9, NULL, 'comparing ', 'exchanging ', 'discussing ', 'sharing', 0, 'D', 26);
INSERT INTO `administrator_subquestion` VALUES (49, 10, NULL, 'accept ', 'know ', 'believe ', 'bother', 0, 'B', 26);
INSERT INTO `administrator_subquestion` VALUES (50, 1, 'asdsadsadadsa', 'asd', 'ASDAS', 'asdeprjeofihdf', '038rhorugdgub', 0, 'B', 29);

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 73 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$260000$mDN6etcp4447r6wlS8rWTb$wOwWWjXOwmCg04hjJUumpHx3bxcGA8rA3on/2L1RFwM=', '2022-05-12 02:40:42.144908', 1, '000', '', '', '', 1, 1, '2022-05-08 09:28:48.678333');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id` ASC, `group_id` ASC) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for client_done_question
-- ----------------------------
DROP TABLE IF EXISTS `client_done_question`;
CREATE TABLE `client_done_question`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `option` varchar(5) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `subQuestion_id` int NOT NULL,
  `wxUser_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `client_done_question_subQuestion_id_a890030e_fk_administr`(`subQuestion_id` ASC) USING BTREE,
  INDEX `client_done_question_wxUser_id_0e84bcc7_fk_client_wxuser_id`(`wxUser_id` ASC) USING BTREE,
  CONSTRAINT `client_done_question_subQuestion_id_a890030e_fk_administr` FOREIGN KEY (`subQuestion_id`) REFERENCES `administrator_subquestion` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `client_done_question_wxUser_id_0e84bcc7_fk_client_wxuser_id` FOREIGN KEY (`wxUser_id`) REFERENCES `client_wxuser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of client_done_question
-- ----------------------------

-- ----------------------------
-- Table structure for client_history
-- ----------------------------
DROP TABLE IF EXISTS `client_history`;
CREATE TABLE `client_history`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `openid` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `date` datetime(6) NOT NULL,
  `question_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `client_history_question_id_fc676cb9_fk_administrator_question_id`(`question_id` ASC) USING BTREE,
  CONSTRAINT `client_history_question_id_fc676cb9_fk_administrator_question_id` FOREIGN KEY (`question_id`) REFERENCES `administrator_question` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of client_history
-- ----------------------------
INSERT INTO `client_history` VALUES (72, 'oXvTf5RYmgjHWMJa6F6PXeETKcUY', '2022-05-11 21:28:59.947719', 20);
INSERT INTO `client_history` VALUES (73, 'oXvTf5RYmgjHWMJa6F6PXeETKcUY', '2022-05-11 21:30:38.377325', 26);
INSERT INTO `client_history` VALUES (74, 'oXvTf5RYmgjHWMJa6F6PXeETKcUY', '2022-05-11 21:30:54.176063', 26);

-- ----------------------------
-- Table structure for client_listofquestion
-- ----------------------------
DROP TABLE IF EXISTS `client_listofquestion`;
CREATE TABLE `client_listofquestion`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `openid` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `question_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `client_listofquestio_question_id_ad68165b_fk_administr`(`question_id` ASC) USING BTREE,
  CONSTRAINT `client_listofquestio_question_id_ad68165b_fk_administr` FOREIGN KEY (`question_id`) REFERENCES `administrator_question` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of client_listofquestion
-- ----------------------------

-- ----------------------------
-- Table structure for client_userapprovesolution
-- ----------------------------
DROP TABLE IF EXISTS `client_userapprovesolution`;
CREATE TABLE `client_userapprovesolution`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` int NOT NULL,
  `solution_id` int NOT NULL,
  `user_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `client_userapproveso_solution_id_dd88f077_fk_administr`(`solution_id` ASC) USING BTREE,
  INDEX `client_userapprovesolution_user_id_3fef8460_fk_client_wxuser_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `client_userapproveso_solution_id_dd88f077_fk_administr` FOREIGN KEY (`solution_id`) REFERENCES `administrator_solution` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `client_userapprovesolution_user_id_3fef8460_fk_client_wxuser_id` FOREIGN KEY (`user_id`) REFERENCES `client_wxuser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of client_userapprovesolution
-- ----------------------------

-- ----------------------------
-- Table structure for client_wrongquestions
-- ----------------------------
DROP TABLE IF EXISTS `client_wrongquestions`;
CREATE TABLE `client_wrongquestions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `openid` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `date` datetime(6) NOT NULL,
  `havedone` tinyint(1) NOT NULL,
  `question_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `client_wrongquestion_question_id_139c740b_fk_administr`(`question_id` ASC) USING BTREE,
  CONSTRAINT `client_wrongquestion_question_id_139c740b_fk_administr` FOREIGN KEY (`question_id`) REFERENCES `administrator_question` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of client_wrongquestions
-- ----------------------------

-- ----------------------------
-- Table structure for client_wxuser
-- ----------------------------
DROP TABLE IF EXISTS `client_wxuser`;
CREATE TABLE `client_wxuser`  (
  `id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `recent_choice` int NOT NULL,
  `recent_cloze` int NOT NULL,
  `recent_reading` int NOT NULL,
  `total_choice` int NOT NULL,
  `right_choice` int NOT NULL,
  `total_cloze` int NOT NULL,
  `right_cloze` int NOT NULL,
  `total_reading` int NOT NULL,
  `right_reading` int NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  CONSTRAINT `check_status` CHECK ((`status` >= 0) and (`status` <= 7)),
  CONSTRAINT `recent_choice__gte_0` CHECK (`recent_choice` >= 0),
  CONSTRAINT `recent_cloze__gte_0` CHECK (`recent_cloze` >= 0),
  CONSTRAINT `recent_reading__gte_0` CHECK (`recent_reading` >= 0),
  CONSTRAINT `right_choice__gte_0` CHECK (`right_choice` >= 0),
  CONSTRAINT `right_cloze__gte_0` CHECK (`right_cloze` >= 0),
  CONSTRAINT `right_reading__gte_0` CHECK (`right_reading` >= 0),
  CONSTRAINT `total_choice__gte_0` CHECK (`total_choice` >= 0),
  CONSTRAINT `total_cloze__gte_0` CHECK (`total_cloze` >= 0),
  CONSTRAINT `total_reading__gte_0` CHECK (`total_reading` >= 0)
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of client_wxuser
-- ----------------------------
INSERT INTO `client_wxuser` VALUES ('oXvTf5evLSrviTOCI76sVx1rmZ9w', 'Guborrow', 0, 0, 0, 10, 1, 90, 17, 90, 21, 0);
INSERT INTO `client_wxuser` VALUES ('oXvTf5RYmgjHWMJa6F6PXeETKcUY', '圍棋少年李霄龍', 0, 0, 0, 13, 2, 40, 13, 0, 0, 0);
INSERT INTO `client_wxuser` VALUES ('oXvTf5UbEhPJFp7drdwl2Sh25n7Q', '楊.', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `client_wxuser` VALUES ('oXvTf5V2MTcsTiiYmIFAfXxuwGDA', '狼来了', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
INSERT INTO `django_admin_log` VALUES (1, '2022-05-12 02:41:19.283711', '1', '343434', 1, '[{\"added\": {}}]', 18, 1);
INSERT INTO `django_admin_log` VALUES (2, '2022-05-12 02:41:23.392159', '1', '343434', 2, '[]', 18, 1);
INSERT INTO `django_admin_log` VALUES (3, '2022-05-12 02:41:38.705883', '1', '343434', 2, '[{\"changed\": {\"fields\": [\"\\u4e3e\\u62a5\\u6570\"]}}]', 18, 1);
INSERT INTO `django_admin_log` VALUES (4, '2022-05-12 02:41:52.226227', '1', '343434', 2, '[{\"changed\": {\"fields\": [\"\\u88ab\\u7ba1\\u7406\\u5458\\u8ba4\\u53ef\\u7684\\u6b21\\u6570\"]}}]', 18, 1);
INSERT INTO `django_admin_log` VALUES (5, '2022-05-12 02:41:59.915210', '1', '343434', 2, '[{\"changed\": {\"fields\": [\"\\u4e3e\\u62a5\\u6570\"]}}]', 18, 1);
INSERT INTO `django_admin_log` VALUES (6, '2022-05-12 02:42:06.805753', '1', '343434', 2, '[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u662f\\u574f\\u9898\\u89e3\"]}}]', 18, 1);
INSERT INTO `django_admin_log` VALUES (7, '2022-05-12 02:43:55.020759', '1', '343434', 3, '', 18, 1);

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (13, 'administrator', 'adminapprovesolution');
INSERT INTO `django_content_type` VALUES (14, 'administrator', 'notice');
INSERT INTO `django_content_type` VALUES (15, 'administrator', 'operationrecord');
INSERT INTO `django_content_type` VALUES (16, 'administrator', 'question');
INSERT INTO `django_content_type` VALUES (18, 'administrator', 'solution');
INSERT INTO `django_content_type` VALUES (17, 'administrator', 'subquestion');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (7, 'client', 'done_question');
INSERT INTO `django_content_type` VALUES (8, 'client', 'history');
INSERT INTO `django_content_type` VALUES (9, 'client', 'listofquestion');
INSERT INTO `django_content_type` VALUES (10, 'client', 'userapprovesolution');
INSERT INTO `django_content_type` VALUES (11, 'client', 'wrongquestions');
INSERT INTO `django_content_type` VALUES (12, 'client', 'wxuser');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2022-05-12 01:14:50.692009');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2022-05-12 01:14:52.317694');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2022-05-12 01:14:52.642904');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2022-05-12 01:14:52.656357');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2022-05-12 01:14:52.667959');
INSERT INTO `django_migrations` VALUES (6, 'administrator', '0001_initial', '2022-05-12 01:14:54.090341');
INSERT INTO `django_migrations` VALUES (7, 'contenttypes', '0002_remove_content_type_name', '2022-05-12 01:14:54.305903');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0002_alter_permission_name_max_length', '2022-05-12 01:14:54.441427');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0003_alter_user_email_max_length', '2022-05-12 01:14:54.579268');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0004_alter_user_username_opts', '2022-05-12 01:14:54.593095');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0005_alter_user_last_login_null', '2022-05-12 01:14:54.703877');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0006_require_contenttypes_0002', '2022-05-12 01:14:54.711673');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0007_alter_validators_add_error_messages', '2022-05-12 01:14:54.723569');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0008_alter_user_username_max_length', '2022-05-12 01:14:54.862464');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0009_alter_user_last_name_max_length', '2022-05-12 01:14:54.993525');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0010_alter_group_name_max_length', '2022-05-12 01:14:55.120058');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0011_update_proxy_permissions', '2022-05-12 01:14:55.140875');
INSERT INTO `django_migrations` VALUES (18, 'auth', '0012_alter_user_first_name_max_length', '2022-05-12 01:14:55.280057');
INSERT INTO `django_migrations` VALUES (19, 'client', '0001_initial', '2022-05-12 01:14:57.488931');
INSERT INTO `django_migrations` VALUES (20, 'sessions', '0001_initial', '2022-05-12 01:14:57.579982');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('qn9ktl7j32hy6haz8uvlawbkjz60l4i6', '.eJxVjDsOwjAQBe_iGlle_0NJzxmsXXuNAyiW8qkQd4dIKaB9M_NeIuG2trQtPKexiLMAcfrdCPODpx2UO063LnOf1nkkuSvyoIu89sLPy-H-HTRc2rcesnJKhQqeIboA4HUYjEZLmQhqBCIHqmhA9uQzx1it0ZYcG0ZbSbw_wZo3ug:1noyks:Tk8SyT_DfExawAIiADsslsivrwbLG385_eeMdkjCaZA', '2022-05-26 02:40:42.153696');

SET FOREIGN_KEY_CHECKS = 1;
