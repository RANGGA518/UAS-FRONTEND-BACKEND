-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: uas_projek
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `kategori`
--

DROP TABLE IF EXISTS `kategori`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kategori` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nama_kategori` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kategori`
--

LOCK TABLES `kategori` WRITE;
/*!40000 ALTER TABLE `kategori` DISABLE KEYS */;
INSERT INTO `kategori` VALUES (1,'Makanan'),(2,'Dapur & Bahan'),(3,'Minuman'),(4,'Ibu & Anak'),(5,'Kesehatan & Kebersihan'),(6,'Kebutuhan Rumah'),(7,'Perawatan Diri');
/*!40000 ALTER TABLE `kategori` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produk`
--

DROP TABLE IF EXISTS `produk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produk` (
  `kode_barang` varchar(10) NOT NULL,
  `nama_barang` varchar(100) DEFAULT NULL,
  `deskripsi` text,
  `stok` int DEFAULT NULL,
  `harga` decimal(12,2) DEFAULT NULL,
  `kategori_id` int DEFAULT NULL,
  `gambar` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`kode_barang`),
  KEY `kategori_id` (`kategori_id`),
  CONSTRAINT `produk_ibfk_1` FOREIGN KEY (`kategori_id`) REFERENCES `kategori` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produk`
--

LOCK TABLES `produk` WRITE;
/*!40000 ALTER TABLE `produk` DISABLE KEYS */;
INSERT INTO `produk` VALUES ('MAK001','Indomie Goreng','Mi instan goreng dengan cita rasa khas yang gurih dan lezat. Cocok dinikmati kapan saja sebagai pilihan praktis dan mengenyangkan.\r\n',10,3500.00,1,'download_2.jpg'),('MAK002','Piatos','Snack keripik kentang dengan rasa rumput laut yang gurih dan renyah. Pilihan camilan ringan untuk menemani waktu santai.',20,10000.00,1,'Jack_n_Jill_Piattos_Crisp_Cheese_Flavored_Potato_Chips_-_85G.jpg'),('MAK003','Sari Roti','Roti tawar lembut dengan isian selai blueberry yang manis dan segar. Cocok untuk sarapan atau bekal sehari-hari.',5,20000.00,1,'download.jpg'),('MAK004','Beng Beng','Wafer cokelat berlapis karamel dan cokelat premium. Nikmat disantap dalam kondisi dingin untuk sensasi rasa yang lebih maksimal.',50,5000.00,1,'Product_Specification___Product_Name....jpg'),('MAK005','Sosis','Sosis siap saji dengan rasa pedas yang mantap dan tekstur kenyal. Cocok untuk digoreng atau dijadikan pelengkap berbagai menu.',70,10000.00,1,'Stack_of_boiled_sausages_isolated_on_white___Premium_Photo.jpg'),('MAK006','Silverqueen','Cokelat batang berkualitas dengan rasa manis dan lembut. Pilihan tepat untuk camilan atau hadiah di berbagai kesempatan.',25,15000.00,1,'ATTENTION__-_GRAMMAR_CHANGES_TO_25_gr_-_NO_ONE_CAN....jpg'),('MAK007','Apel','Buah apel segar berkualitas pilihan yang dijual per buah. Rasanya manis dan segar, cocok untuk konsumsi harian yang sehat.\r\n',30,15000.00,1,'apel.jpg'),('MAK008','Roti Gandum','Roti gandum lembut dengan isian selai gandum yang melimpah. Cocok untuk gaya hidup sehat dan menu sarapan bergizi.',80,5000.00,1,'Roma_Sari_Wheat_Biscuits_Roll_-_Netto_149_gr.jpg');
/*!40000 ALTER TABLE `produk` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `username_2` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (13,'angg','ranggaardiansyah518@gmail.com','rangga123'),(14,'ang','ranggaardiansyah518@gmail.com','rangga123'),(15,'ring','ringgo123@gmail.com','ring123456');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-20  9:26:40
