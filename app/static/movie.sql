-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: movie
-- ------------------------------------------------------
-- Server version	5.7.17-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `is_super` smallint(6) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `role_id` (`role_id`),
  KEY `ix_admin_addtime` (`addtime`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'superadmin','pbkdf2:sha256:50000$nEH42T2u$138bc5ba54bd35137cf9c01e74d16e56359cff20fb841550a7ec3f52155ba137',0,5,'2018-11-30 14:38:32'),(6,'tagadmin1','pbkdf2:sha256:50000$jODO6ag8$8dbb9e8721551e42e1990674029beacdc8759daa1afefe020dd706bd1fd05fc5',1,6,'2018-12-11 14:14:39'),(7,'movieadmin1','pbkdf2:sha256:50000$yKjNywVj$642b00ba7515a365fa4cf40a15155f7b563b06b8b12f41f38b3f2a74ebc06617',1,7,'2018-12-11 14:28:18'),(8,'previewadmin1','pbkdf2:sha256:50000$ONLWT07m$ed134918629bfea7ba80cd4c948147a23d8b58907b79c44b11d16bb7a8e8433f',1,8,'2018-12-11 14:46:28'),(9,'useradmin1','pbkdf2:sha256:50000$mrGq1lV0$e8cb5ddf6cd6145b6ea8799a0df29504e84bf6a7026f88857afbeadaf4ede9f9',1,9,'2018-12-11 14:46:55'),(10,'commentadmin1','pbkdf2:sha256:50000$qrYuRfqm$1124aee4f114b67bdd19df9f92ad6a926c3c9558da85f38f6b8c85d60de09f6a',1,10,'2018-12-11 14:47:15'),(11,'moviecoladmin1','pbkdf2:sha256:50000$fLECRJGB$dbb72f4be9f5b073dea87cb903633a6c7ef2686d5d5c4288977e2354a9b14761',1,11,'2018-12-11 14:47:35'),(12,'logadmin1','pbkdf2:sha256:50000$iqFBxZeG$4d0152c78b2536da40714caaac3dc0832b8f60d3f3732b520dacc8fc200762ec',1,12,'2018-12-11 14:47:49'),(13,'roleadmin1','pbkdf2:sha256:50000$zpSHiTNH$55e6d56f7da87d570912bcbc7e7a559a0194a41d1a3f5817206219375efdeaf9',1,13,'2018-12-11 14:48:03'),(14,'authadmin1','pbkdf2:sha256:50000$boDNaZdg$d20410e0e984ddaf55ae4eaf9e057c16d43506190f0fd41c931d9572cec8d53b',1,14,'2018-12-11 14:48:21'),(15,'adminadmin1','pbkdf2:sha256:50000$bUskHYi2$d8b5372bdadafb7acb8a52452d8ad515080f51d12f4be8347dd4281d2339fa8f',1,15,'2018-12-11 14:48:42');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adminlog`
--

DROP TABLE IF EXISTS `adminlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adminlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_adminlog_addtime` (`addtime`),
  CONSTRAINT `adminlog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminlog`
--

LOCK TABLES `adminlog` WRITE;
/*!40000 ALTER TABLE `adminlog` DISABLE KEYS */;
INSERT INTO `adminlog` VALUES (1,1,'127.0.0.1','2018-12-07 18:04:02'),(2,1,'127.0.0.1','2018-12-07 18:04:40'),(3,1,'127.0.0.1','2018-12-07 21:43:14'),(4,1,'127.0.0.1','2018-12-10 11:40:14'),(5,1,'127.0.0.1','2018-12-11 12:25:47'),(6,1,'127.0.0.1','2018-12-11 13:32:22'),(7,1,'127.0.0.1','2018-12-11 14:13:04'),(8,6,'127.0.0.1','2018-12-11 14:15:42'),(9,1,'127.0.0.1','2018-12-11 14:18:13'),(10,1,'127.0.0.1','2018-12-11 14:18:29'),(11,6,'127.0.0.1','2018-12-11 14:20:37'),(12,1,'127.0.0.1','2018-12-11 14:30:40'),(13,1,'127.0.0.1','2018-12-11 14:30:56'),(14,8,'127.0.0.1','2018-12-11 14:49:39'),(15,8,'127.0.0.1','2018-12-11 14:52:33'),(16,1,'127.0.0.1','2018-12-11 14:53:04'),(17,14,'127.0.0.1','2018-12-11 14:59:57'),(18,1,'127.0.0.1','2018-12-11 15:00:30'),(19,8,'127.0.0.1','2018-12-11 15:04:51'),(20,1,'127.0.0.1','2018-12-12 15:18:12');
/*!40000 ALTER TABLE `adminlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth`
--

DROP TABLE IF EXISTS `auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `url` (`url`),
  KEY `ix_auth_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth`
--

LOCK TABLES `auth` WRITE;
/*!40000 ALTER TABLE `auth` DISABLE KEYS */;
INSERT INTO `auth` VALUES (6,'添加标签','/admin/tag/add/','2018-12-10 13:58:14'),(8,'删除标签','/admin/tag/del/<int:id>/<int:page>/','2018-12-10 14:38:18'),(9,'编辑标签','/admin/tag/edit/<int:id>/','2018-12-10 14:38:38'),(10,'添加电影','/admin/movie/add/','2018-12-11 13:02:41'),(11,'删除电影','/admin/movie/del/<int:id>/<int:page>/','2018-12-11 13:03:18'),(12,'编辑电影','/admin/movie/edit/<int:id>/','2018-12-11 13:03:40'),(13,'标签列表','/admin/tag/list/<int:page>/','2018-12-11 14:21:38'),(14,'电影列表','/admin/movie/list/<int:page>/','2018-12-11 14:25:18'),(15,'添加预告','/admin/preview/add/','2018-12-11 14:32:03'),(16,'编辑预告','/admin/preview/edit/<int:id>/','2018-12-11 14:32:25'),(17,'删除预告','/admin/preview/del/<int:id>/<int:page>/','2018-12-11 14:32:39'),(18,'预告列表','/admin/preview/list/<int:page>/','2018-12-11 14:32:54'),(19,'会员查看','/admin/user/view/<int:id>/','2018-12-11 14:35:43'),(20,'会员删除','/admin/user/del/<int:id>/<int:page>/','2018-12-11 14:35:54'),(21,'会员列表','/admin/user/list/<int:page>/','2018-12-11 14:36:05'),(22,'评论删除','/admin/comment/del/<int:id>/<int:page>/','2018-12-11 14:36:16'),(23,'评论列表','/admin/comment/list/<int:page>/','2018-12-11 14:36:28'),(24,'电影收藏删除','/admin/moviecol/del/<int:id>/<int:page>/','2018-12-11 14:36:39'),(25,'电影收藏列表','/admin/moviecol/list/<int:page>/','2018-12-11 14:36:49'),(26,'操作日志列表','/admin/oplog/list/<int:page>/','2018-12-11 14:37:00'),(27,'管理员登录日志列表','/admin/adminloginlog/list/<int:page>/','2018-12-11 14:37:10'),(28,'用户登录日志列表','/admin/userloginlog/list/<int:page>/','2018-12-11 14:37:24'),(30,'角色添加','/admin/role/add/','2018-12-11 14:37:58'),(31,'角色删除','/admin/role/del/<int:id>/<int:page>/','2018-12-11 14:38:14'),(32,'角色编辑','/admin/role/edit/<int:id>/','2018-12-11 14:38:24'),(33,'角色列表','/admin/role/list/<int:page>/','2018-12-11 14:38:36'),(34,'权限添加','/admin/auth/add/','2018-12-11 14:38:49'),(35,'权限编辑','/admin/auth/edit/<int:id>/','2018-12-11 14:39:04'),(36,'权限删除','/admin/auth/del/<int:id>/<int:page>/','2018-12-11 14:39:16'),(37,'权限列表','/admin/auth/list/<int:page>/','2018-12-11 14:39:55'),(38,'管理员添加','/admin/admin/add/','2018-12-11 14:40:08'),(39,'管理员列表','/admin/admin/list/<int:page>/','2018-12-11 14:40:21');
/*!40000 ALTER TABLE `auth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `movie_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_comment_addtime` (`addtime`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (20,'好看好看哈哈哈',16,16,'2018-12-13 14:49:42'),(21,'好看哈哈',15,16,'2018-12-13 14:50:56'),(22,'哈哈',15,16,'2018-12-13 14:51:07'),(23,'哈哈哈哈哈哈',15,16,'2018-12-13 14:52:57'),(24,'啊啊啊',15,16,'2018-12-13 14:54:56');
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movie`
--

DROP TABLE IF EXISTS `movie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `info` text,
  `logo` varchar(255) DEFAULT NULL,
  `star` smallint(6) DEFAULT NULL,
  `playnum` bigint(20) DEFAULT NULL,
  `commentnum` bigint(20) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `release_time` date DEFAULT NULL,
  `length` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `url` (`url`),
  UNIQUE KEY `logo` (`logo`),
  KEY `tag_id` (`tag_id`),
  KEY `ix_movie_addtime` (`addtime`),
  CONSTRAINT `movie_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movie`
--

LOCK TABLES `movie` WRITE;
/*!40000 ALTER TABLE `movie` DISABLE KEYS */;
INSERT INTO `movie` VALUES (15,'电影1的名称','201812121702587e9b607594be48ffbb0f11fb15937125.mp4','这是电影1的简介','2018121217025807a033387aee4606b00ddbda921df5d6.jpg',4,20,4,36,'中国','2018-12-27','12','2018-12-12 17:02:59'),(16,'电影2的名称','201812121704055eb83ee54cce4a39a5bb4f538f3b22c2.mp4','这是电影2的简介','20181212170405a59277da87374f749ccc1ca4f5229234.jpg',3,17,2,37,'法国','2018-12-31','13','2018-12-12 17:04:05');
/*!40000 ALTER TABLE `movie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `moviecol`
--

DROP TABLE IF EXISTS `moviecol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `moviecol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_moviecol_addtime` (`addtime`),
  CONSTRAINT `moviecol_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `moviecol_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moviecol`
--

LOCK TABLES `moviecol` WRITE;
/*!40000 ALTER TABLE `moviecol` DISABLE KEYS */;
INSERT INTO `moviecol` VALUES (14,16,17,'2018-12-13 17:34:33');
/*!40000 ALTER TABLE `moviecol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oplog`
--

DROP TABLE IF EXISTS `oplog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oplog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `reason` varchar(600) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_oplog_addtime` (`addtime`),
  CONSTRAINT `oplog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oplog`
--

LOCK TABLES `oplog` WRITE;
/*!40000 ALTER TABLE `oplog` DISABLE KEYS */;
INSERT INTO `oplog` VALUES (1,1,'127.0.0.1','添加标签asdfasdf','2018-12-07 17:53:59'),(2,1,'127.0.0.1','添加标签za','2018-12-10 14:49:59'),(3,1,'127.0.0.1','添加标签科幻','2018-12-12 16:52:02'),(4,1,'127.0.0.1','添加标签动作','2018-12-12 16:52:08'),(5,1,'127.0.0.1','添加标签爱情','2018-12-12 16:52:13');
/*!40000 ALTER TABLE `oplog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `preview`
--

DROP TABLE IF EXISTS `preview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `preview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `logo` (`logo`),
  KEY `ix_preview_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `preview`
--

LOCK TABLES `preview` WRITE;
/*!40000 ALTER TABLE `preview` DISABLE KEYS */;
INSERT INTO `preview` VALUES (6,'selena1','2018121215185839ef9fe30a8b42cdae6b3ae12d3961d6.jpg','2018-12-12 15:18:59'),(7,'selena2','20181212151928baa5d0f1a60543139912db13296a6b07.jpg','2018-12-12 15:19:29'),(8,'shu1','20181212151955302eef452db944f2b94bd9a4663920c9.jpg','2018-12-12 15:19:55'),(9,'gou1','2018121215202293fdd4010d7e436b932854abf0b89043.jpg','2018-12-12 15:20:23'),(10,'gou2','20181212152035feca444338d54d49bf31a31ea7a4de25.jpg','2018-12-12 15:20:35');
/*!40000 ALTER TABLE `preview` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `auths` varchar(600) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_role_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (5,'超级管理员','6,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,30,31,32,33,34,35,36,37,38,39','2018-12-11 13:00:59'),(6,'标签管理','6,8,9,13','2018-12-11 13:02:06'),(7,'电影管理','10,11,12,14','2018-12-11 13:05:27'),(8,'预告管理','15,16,17,18','2018-12-11 14:42:10'),(9,'会员管理','19,20,21','2018-12-11 14:42:42'),(10,'评论管理','22,23','2018-12-11 14:43:05'),(11,'电影收藏管理','24,25','2018-12-11 14:43:24'),(12,'日志管理','26,27,28','2018-12-11 14:43:54'),(13,'角色管理','30,31,32,33','2018-12-11 14:44:17'),(14,'权限管理','34,35,36,37','2018-12-11 14:44:48'),(15,'管理员管理','38,39','2018-12-11 14:44:58');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_tag_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
INSERT INTO `tag` VALUES (36,'科幻','2018-12-12 16:52:02'),(37,'动作','2018-12-12 16:52:08'),(38,'爱情','2018-12-12 16:52:13');
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `info` text,
  `face` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  `uuid` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `face` (`face`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_user_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'蛇','123','1211@123.com','13812341231','蛇','1f40d.png','2018-12-07 15:03:58','6dd65bd257e2449aa21babbbaabd3ef1'),(2,'鼠','123','1212@123.com','13812341232','鼠','1f401.png','2018-12-07 15:03:58','6dd65bd257e2449aa21babbbaabd3ef2'),(3,'牛','123','1213@123.com','13812341233','牛','1f402.png','2018-12-07 15:03:58','6dd65bd257e2449aa21babbbaabd3ef3'),(4,'虎','123','1214@123.com','13812341234','虎','1f405.png','2018-12-07 15:03:58','6dd65bd257e2449aa21babbbaabd3ef4'),(5,'兔','123','1215@123.com','13812341235','兔','1f407.png','2018-12-07 15:03:58','6dd65bd257e2449aa21babbbaabd3ef5'),(6,'龙','123','1216@123.com','13812341236','龙','1f409.png','2018-12-07 15:03:58','6dd65bd257e2449aa21babbbaabd3ef6'),(7,'羊','123','1217@123.com','13812341237','羊','1f411.png','2018-12-07 15:03:58','6dd65bd257e2449aa21babbbaabd3ef7'),(8,'猴','123','1218@123.com','13812341238','猴','1f412.png','2018-12-07 15:03:58','6dd65bd257e2449aa21babbbaabd3ef8'),(9,'鸡','123','1219@123.com','13812341239','鸡','1f413.png','2018-12-07 15:03:58','6dd65bd257e2449aa21babbbaabd3ef9'),(12,'马','123','1222@123.com','13812341242','马','1f434.png','2018-12-07 15:03:59','6dd65bd257e2449aa21babbbaabd3eg3'),(13,'狗','123','1220@123.com','13812341240','狗','1f415.png','2018-12-07 15:39:22','6dd65bd257e2449aa21babbbaabd3eg1'),(14,'猪','123','1221@123.com','13812341241','猪','1f416.png','2018-12-07 15:40:02','6dd65bd257e2449aa21babbbaabd3eg2'),(16,'xiaoming','pbkdf2:sha256:50000$IGlc7hGn$74d519495b75481923817a0659d51c190ed09f923c90f054dce2a82a80361dac','2197799191@qq.com','13345678901','xiaominghaa','20181212145326b1c7c215a3f2488f891916e05dfbcfbb','2018-12-12 14:51:08','c3f6b022044f42eb837c78ca6b228997'),(17,'479','pbkdf2:sha256:50000$EfRN3H1L$b275a2cf804d9aaa430a58e3eac2580582afae23819ae8fa17798927163c3588','283275935@qq.com','18518230335',NULL,NULL,'2018-12-13 15:24:26','849884adf3ca4a6990f663d59fb93433');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userlog`
--

DROP TABLE IF EXISTS `userlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_userlog_addtime` (`addtime`),
  CONSTRAINT `userlog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userlog`
--

LOCK TABLES `userlog` WRITE;
/*!40000 ALTER TABLE `userlog` DISABLE KEYS */;
INSERT INTO `userlog` VALUES (1,1,'192.168.4.1','2018-12-07 18:12:33'),(2,2,'192.168.4.2','2018-12-07 18:12:33'),(3,3,'192.168.4.3','2018-12-07 18:12:33'),(4,4,'192.168.4.4','2018-12-07 18:12:33'),(5,5,'192.168.4.5','2018-12-07 18:12:33'),(6,6,'192.168.4.6','2018-12-07 18:12:33'),(7,7,'192.168.4.7','2018-12-07 18:12:33'),(8,8,'192.168.4.8','2018-12-07 18:12:33'),(9,9,'192.168.4.9','2018-12-07 18:12:35'),(10,NULL,'127.0.0.1','2018-12-11 18:01:39'),(11,NULL,'127.0.0.1','2018-12-12 14:02:10'),(12,NULL,'127.0.0.1','2018-12-12 14:17:36'),(13,16,'127.0.0.1','2018-12-12 14:51:14'),(14,16,'127.0.0.1','2018-12-12 14:53:19'),(15,16,'127.0.0.1','2018-12-12 15:06:19'),(16,16,'127.0.0.1','2018-12-13 14:25:37'),(17,17,'127.0.0.1','2018-12-13 15:24:38'),(18,16,'127.0.0.1','2018-12-13 15:36:34'),(19,17,'127.0.0.1','2018-12-13 17:34:49');
/*!40000 ALTER TABLE `userlog` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-12-18 15:23:03
