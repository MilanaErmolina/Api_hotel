-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: hotel_booking
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `hotel`
--

DROP TABLE IF EXISTS `hotel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `rating` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotel`
--

LOCK TABLES `hotel` WRITE;
/*!40000 ALTER TABLE `hotel` DISABLE KEYS */;
INSERT INTO `hotel` VALUES (1,'Гранд Отель Европа','ул. Тверская, 10','Москва',4.8),(2,'Гранд Отель Европа','ул. Тверская, 10','Москва',4.8),(3,'Ритц Карлтон','ул. Тверская, 3','Москва',4.5),(4,'Ритц Карлтон','ул. Тверская, 3','Москва',4.9),(5,'Арарат Парк Хаятт','ул. Неглинная, 4','Москва',4.9),(6,'Астория','ул. Большая Морская, 39','Санкт-Петербург',4.8),(7,'Коринтия Санкт-Петербург','Невский проспект, 57','Санкт-Петербург',4.6),(8,'Гранд Отель Европа','ул. Тверская, 10','Москва',4.8),(9,'Ритц Карлтон','ул. Тверская, 3','Москва',4.7),(10,'Арарат Парк Хаятт','ул. Неглинная, 4','Москва',4.9),(11,'Астория','ул. Большая Морская, 39','Санкт-Петербург',4.8),(12,'Коринтия','Невский проспект, 57','Санкт-Петербург',4.6),(13,'Сочи Парк Отель','ул. Навагинская, 9','Сочи',4.7),(21,'Гранд Отель ','ул. Тверская, 10','Москва',4.8),(22,'Гранд отель','ул. Тверская, 10','Москва',4.7),(23,'Отель','ул. Ленина, 14','Кострома',4.5),(24,'Отель','ул. Ленина, 14','Кострома',4.5),(26,'Отель 3','ул. Ленина, 14','Кострома',4.5),(27,'Отель 3','ул. Ленина, 14','Кострома',4.5);
/*!40000 ALTER TABLE `hotel` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-18  0:34:57
