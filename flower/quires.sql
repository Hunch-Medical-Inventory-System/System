-- MySQL dump 10.13  Distrib 5.7.42, for Linux (aarch64)
--
-- Host: 127.0.0.1    Database: inv
-- ------------------------------------------------------
-- Server version	5.7.42-0ubuntu0.18.04.1

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
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES ('123','A',5,'2026-01-01','ABC'),('123','A',10,'2027-01-01','ABC'),('311673188538','Pharmacy Center',4,'2026-02-18','Asprin'),('311673188538','Pharmacy Center',315,'2026-03-14','Aspirin'),('311673188538','Pharmacy Center',315,'2026-04-11','Aspirin'),('311673188538','Pharmacy Center',315,'2026-05-08','Aspirin'),('311673188538','Pharmacy Center',4,'2026-05-09','Acetaminophen'),('68387-214','Pharmacy Center',51,'2026-05-09','Acetaminophen'),('GUMMY-BEAR','Warren Tech AA11',28,'2026-03-13','Gummy Bear'),('MIKE-N-IKE','Warren Tech B2',29,'2026-02-24','Mike & Ike'),('SKITTLES','Warren Tech D4',22,'2026-02-25','Skittles'),('STARBURSTS','Warren Tech C3',28,'2026-02-25','Starburst'),('WK2XYI10QM','Locker 1313',15,'2026-03-04','Ibuprofen'),('WK2XYI10QM','Locker 1313',5,'2026-03-06','Ibuprofen');
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT INTO `logs` VALUES ('00988951-7dc6-41bc-a9e1-5acf3b62e6a3','admin','2026-02-21 00:00:00','Warehouse A','Removed 100 of UPID123'),('03100f60-b279-4c46-a67d-572ec4e1effc','123','2026-01-28 00:00:00','A1','Inserted 10 of Sample Item (UPID: UPID123) into inventory at A1, expiring on 2025-01-07.'),('0582a181-7edb-4008-bdeb-9a40ba3bc721','admin','2026-05-04 00:00:00','A','Added 2 of 123'),('05ecc222-503e-451a-b9f9-fefada751f7d','admin','2026-02-25 00:00:00','Warren Tech D4','Removed 1 of SKITTLES'),('08ffeb2a-cd5b-4c8b-8bcd-9a5c6008def1','admin','2026-02-25 00:00:00','Warren Tech AA11','Removed 1 of GUMMY-BEAR'),('0f106bff-89ba-4434-b512-a8f01054968d','78b3833f-a0b3-423c-a03f-8633b4187420','2026-01-29 00:00:00','userData','Retrieved history data.'),('10f5d47e-d946-4ebc-862f-c4bea01e5b6b','admin','2026-02-24 00:00:00','Warren Tech B2','Added 1 of MIKE-N-IKE'),('1216b9bb-8734-4cbb-aeb1-c0f804c21bb8','admin','2026-02-21 00:00:00','A1','Removed 10 of UPID12355'),('183e91ae-bf35-4307-a1b2-019429640f9d','admin','2026-05-04 00:00:00','A','Added 3 of 123'),('187f9f07-0276-4ba5-ba57-021d4b9cc93b','admin','2026-02-21 00:00:00','Warehouse A','Removed 99 of UPID123'),('1895d805-a26f-4f42-bcab-58dcfc961e01','admin','2026-02-21 00:00:00','Warehouse A','Removed 1 of UPID123'),('1c2f41ec-0fae-4b1f-875d-ca638d39fd0b','admin','2026-02-25 00:00:00','Warren Tech B2','Added 30 of MIKE-N-IKE'),('20aa7ad6-9310-4e34-a2e2-53c95b1cf1e1','admin','2026-04-29 00:00:00','Pharmacy Center','Added 315 of 311673188538'),('25da8432-506a-45de-bc8b-d48e525efcd1','admin','2026-02-25 00:00:00','Warren Tech D4','Removed 1 of SKITTLES'),('29ebdf0b-ccae-4ed6-bbf1-7d34da2ace04','admin','2026-05-04 00:00:00','2','Removed 2 of 2'),('2d0d618f-26a0-40d6-b9c8-7b0a53275909','admin','2026-02-25 00:00:00','Warren Tech D4','Removed 1 of SKITTLES'),('2fef20a1-1d2d-4caa-bf4e-783d21a2a25a','admin','2026-02-25 00:00:00','Warren Tech C3','Added 30 of STARBURSTS'),('35b49d2b-b008-40af-92ed-7a3dd42e277c','admin','2026-02-24 00:00:00','Warren Tech AA11','Removed 5 of GUMMY-BEAR'),('36baf73b-786f-49a8-9734-78f0e97028f3','123','2026-01-28 00:00:00','A1','Inserted 10 of Sample Item (UPID: UPID1235) into inventory at A1, expiring on 2025-01-07.'),('3cc325a0-429d-44e0-9b5c-fd9b41cd66d3','admin','2026-02-24 00:00:00','Warren Tech C3','Added 1 of STARBURSTS'),('3f0becf2-ccc1-42ed-9a17-c42f73a75713','admin','2026-02-21 00:00:00','Warren Tech','Removed 20 of 345'),('42089e30-b651-434a-8c91-f8db1c8282ff','78b3833f-a0b3-423c-a03f-8633b4187420','2026-01-29 00:00:00','userData','Retrieved history data.'),('42951a7e-5455-4fd3-b901-5750b936ad7b','admin','2026-05-04 00:00:00','B','Removed 3 of 234'),('45d153e0-baa1-4e88-a203-ffe3b4c4ad4f','admin','2026-02-21 00:00:00','Warren Tech AA11','Added 1 of GUMMY-BEAR (Gummy Bear)'),('5192ad17-9655-4896-be8a-1bfa8916873d','admin','2026-05-04 00:00:00','A','Added 5 of 123'),('51a99fcb-523d-4fa0-b4ec-da7bc629597c','admin','2026-02-21 00:00:00','Warren Tech AA11','Added 20 of GUMMY-BEAR (Gummy Bear)'),('5c88569a-bc64-428e-932d-45e42ed737c6','admin','2026-02-24 00:00:00','Warren Tech AA11','Removed 1 of GUMMY-BEAR'),('65b5ebec-149b-43ec-affc-c50273ddd9a3','78b3833f-a0b3-423c-a03f-8633b4187420','2026-01-29 00:00:00','userData','Retrieved history data.'),('675b10a7-eed4-42ae-8219-3da34e2b22c1','system','2026-01-29 00:00:00','userData','Updated user history: 78b3833f-a0b3-423c-a03f-8633b4187420.'),('69c6395a-9746-4eb7-8e67-e340d70d41c6','admin','2026-02-25 00:00:00','Warren Tech D4','Removed 1 of SKITTLES'),('6edb3cb1-cdc2-4043-800e-6fa5d30de618','admin','2026-02-25 00:00:00','Warren Tech B2','Removed 1 of MIKE-N-IKE'),('72b4f980-b312-4644-b59f-323953f7d096','admin','2026-02-25 00:00:00','Warren Tech D4','Removed 1 of SKITTLES'),('73eac0e6-aaf2-43c1-a23e-71ef21c142c6','c65ab095-b75b-4e39-ade1-c2df2387dae2','2026-01-29 00:00:00','userData','Retrieved history data.'),('73f06fd1-d949-4718-bd9e-5e70caca3fd8','admin','2026-02-25 00:00:00','Warren Tech AA11','Added 15 of GUMMY-BEAR'),('765ba76b-5fbf-43a6-92cc-3721c7d5bb84','admin','2026-02-21 00:00:00','Pharmacy Center','Added 50 of 68387-214'),('77559ebf-c25c-4eaa-9770-c7bc760b68b6','c65ab095-b75b-4e39-ade1-c2df2387dae2','2026-01-29 00:00:00','userData','Retrieved history data.'),('794b949f-b99b-4b0a-99dd-e1059981acd4','admin','2026-02-21 00:00:00','Pharmacy Center','Added 4 of 311673188538'),('8043e84e-ba4f-4167-808d-60728b17a034','admin','2026-05-04 00:00:00','2','Added 2 of 2'),('923a5e27-7949-403f-92b8-e2b25bf402a9','admin','2026-02-25 00:00:00','Warren Tech D4','Removed 1 of SKITTLES'),('931f0280-f838-401c-8612-98a04bb0e481','system','2026-01-29 00:00:00','userData','Registered new user: testuser.'),('93828580-0c7a-4cf3-9b76-b7b84459cb86','123','2026-01-28 00:00:00','A1','Inserted 10 of Sample Item (UPID: UPID12355) into inventory at A1, expiring on 2025-01-07.'),('95a2bfd7-4343-44ab-8be6-94b1992d0a04','admin','2026-02-21 00:00:00','Warren Tech','Added 20 of 345'),('95d5d1ae-6722-4827-b9ee-a5f7a7efe470','admin','2026-05-04 00:00:00','Pharmacy Center','Added 2 of 311673188538'),('9c643ef8-4b62-491d-ad37-78344ea753c2','admin','2026-02-25 00:00:00','Warren Tech B2','Removed 1 of MIKE-N-IKE'),('a159dfcc-0060-4a0d-902c-01648226e8be','admin','2026-04-29 00:00:00','Pharmacy Center','Added 1 of 68387-214'),('a8823d85-15b7-4298-93e8-562b80566dc2','admin','2026-02-25 00:00:00','Warren Tech D4','Added 30 of SKITTLES'),('aa0949f4-8b22-4bd4-9fb4-4ba8deffc59a','admin','2026-02-25 00:00:00','Warren Tech D4','Removed 1 of SKITTLES'),('b077af59-6683-4d1b-b865-05ef9dc87f03','78b3833f-a0b3-423c-a03f-8633b4187420','2026-01-29 00:00:00','userData','Retrieved history data.'),('b4358eda-18d0-47ba-953e-690719439889','admin','2026-02-21 00:00:00','Locker 1313','Added 5 of WK2XYI10QM'),('b4dfbefd-6665-48ac-8632-3555c9dac14a','admin','2026-02-21 00:00:00','A1','Removed 10 of UPID1235'),('b700556c-37e9-41ae-aa2f-8a525f35c5ab','admin','2026-02-21 00:00:00','Locker 1313','Added 15 of WK2XYI10QM'),('b81094dc-bfae-434c-a83e-24e469f393d0','admin','2026-05-04 00:00:00','Pharmacy Center','Added 2 of 311673188538'),('bf310fae-1f6e-4ab0-afee-4277f6fa0ba8','admin','2026-02-25 00:00:00','Warren Tech C3','Removed 1 of STARBURSTS'),('c13e5298-215c-41b6-9349-b25d5af100fe','admin','2026-04-29 00:00:00','Pharmacy Center','Added 300 of 311673188538'),('c48c8b74-9834-4091-860c-555b74ca84ca','c65ab095-b75b-4e39-ade1-c2df2387dae2','2026-01-29 00:00:00','userData','Retrieved history data.'),('cf767b5e-4000-4827-a3c7-fbe3f403c263','78b3833f-a0b3-423c-a03f-8633b4187420','2026-01-29 00:00:00','userData','Retrieved history data.'),('d29c8b25-45f3-4287-8546-a7fdefffd141','admin','2026-02-25 00:00:00','Warren Tech C3','Removed 1 of STARBURSTS'),('d2a7f333-6d10-4f74-98d5-52f8f5e66e2b','admin','2026-05-04 00:00:00','A','Added 2 of 123'),('d5b7f57e-ba7a-413b-96ef-a7b59a57bdc6','admin','2026-02-25 00:00:00','Warren Tech D4','Removed 1 of SKITTLES'),('d7f8bff5-eef3-4d24-9199-d22cff737b42','system','2026-01-29 00:00:00','userData','Registered new user: testuser.'),('dd390af8-20db-4114-b65d-483488058e04','admin','2026-02-25 00:00:00','Warren Tech C3','Removed 1 of STARBURSTS'),('df3c6885-4660-4adb-a524-50f07060ffa7','admin','2026-04-29 00:00:00','Pharmacy Center','Added 315 of 311673188538'),('e3fbfb4f-df38-437a-bd99-a85b5e6e7f10','admin','2026-05-04 00:00:00','A','Added 3 of 123'),('eaf36771-2d67-4e7d-af07-06e1019a4114','admin','2026-02-25 00:00:00','Warren Tech AA11','Removed 1 of GUMMY-BEAR'),('ebbc2b2e-f6c4-4831-865f-8e58eab28bf9','admin','2026-02-21 00:00:00','A1','Removed 10 of UPID123'),('ee34c422-0290-4192-b40c-e10d317897a0','admin','2026-05-04 00:00:00','B','Added 3 of 234'),('f4a03dbf-d738-482e-a602-77127c6b6ca3','admin','2026-02-25 00:00:00','Warren Tech D4','Removed 1 of SKITTLES'),('fb8f18fb-9df5-4db3-a400-c339be94a8eb','admin','2026-02-24 00:00:00','Warren Tech D4','Added 1 of SKITTLES'),('fdecb041-e97c-4391-b2d4-95336add3ba3','admin','2026-02-21 00:00:00','Pharmacy Center','Added 15 of 311673188538');
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `med-info`
--

LOCK TABLES `med-info` WRITE;
/*!40000 ALTER TABLE `med-info` DISABLE KEYS */;
/*!40000 ALTER TABLE `med-info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `site-info`
--

LOCK TABLES `site-info` WRITE;
/*!40000 ALTER TABLE `site-info` DISABLE KEYS */;
/*!40000 ALTER TABLE `site-info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('78b3833f-a0b3-423c-a03f-8633b4187420','testuser','testpassword','','{\"date\": \"2026-01-29\", \"description\": \"No Description Inserted\"}');
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

-- Dump completed on 2026-05-04  5:54:42
