-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: jobshield
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Current Database: `jobshield`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `jobshield` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `jobshield`;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `company_name` varchar(150) NOT NULL,
  `job_title` varchar(150) NOT NULL,
  `recruiter_name` varchar(150) DEFAULT NULL,
  `job_url` text,
  `salary` varchar(100) DEFAULT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `jobs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (1,1,'sdgs','vdsss','sdvds','','dvssd','vds','2026-09-13 13:10:45'),(2,1,'ABC Technologies','Software Developer','','','₹5,00,000 per year','We are looking for a software developer with knowledge of Python, HTML, CSS and databases. Candidates should have good programming skills and communication skills.','2026-09-13 13:12:52'),(3,1,'ABC Careers','Data Entry Operator','Rahul','https://example.com/job','₹50,000 per month','Urgent hiring! No experience required. Earn money fast.\r\nPay ₹5,000 registration fee to confirm your position.\r\nContact only on WhatsApp. Send your bank account details\r\nand OTP for salary verification.','2026-09-13 13:15:17'),(4,1,'ABC Online Services','Work From Home Data Entry','HR Manager','','₹50,000 per day','Urgent hiring for work from home data entry jobs.\r\n\r\nNo experience required.\r\n\r\nEarn ₹50000 per day.\r\n\r\nPay ₹3000 registration fee to confirm your position.\r\n\r\nContact only through WhatsApp.\r\n\r\nSend your bank details and OTP for verification.','2026-09-13 14:00:27'),(5,2,'Microsoft','Software Engineer','Sarah Johnson','https://careers.microsoft.com/','₹12,00,000 – ₹18,00,000 per year','Microsoft is hiring a Software Engineer to join its engineering team.\r\n\r\nResponsibilities include developing and maintaining software applications,\r\nwriting clean and reliable code, participating in code reviews, testing\r\nsoftware, and collaborating with other engineers.\r\n\r\nRequirements:\r\nBachelor\'s degree in Computer Science or a related field.\r\nKnowledge of Python, Java, or C++.\r\nGood problem-solving and communication skills.\r\nExperience with software development is preferred.\r\n\r\nCandidates can apply through the official Microsoft careers website.\r\nNo application fee or payment is required.','2026-09-14 03:40:02'),(6,2,'Microsoft','Software Engineer','Sarah Johnson','https://careers.microsoft.com/','₹12,00,000 – ₹18,00,000 per year','Microsoft is hiring a Software Engineer to join its engineering team.\r\n\r\nResponsibilities include developing and maintaining software applications,\r\nwriting clean and reliable code, participating in code reviews, testing\r\nsoftware, and collaborating with other engineers.\r\n\r\nRequirements:\r\nBachelor\'s degree in Computer Science or a related field.\r\nKnowledge of Python, Java, or C++.\r\nGood problem-solving and communication skills.\r\nExperience with software development is preferred.\r\n\r\nCandidates can apply through the official Microsoft careers website.\r\nNo application fee or payment is required.','2026-09-14 03:40:02'),(7,2,'Microsoft','Software Engineer','Microsoft Recruitment Team','https://careers.microsoft.com/','₹8,00,000 – ₹12,00,000 per annum','We are looking for a Software Engineer to join our engineering team. The candidate will be responsible for developing, testing, and maintaining software applications. Candidates should have knowledge of programming languages such as Python, Java, or C++, problem-solving skills, and good communication abilities. The position includes collaboration with engineering teams and participation in the software development lifecycle.','2026-09-17 11:29:23'),(8,2,'Microsoft','Software Engineer','Microsoft Recruitment Team','https://careers.microsoft.com/','₹8,00,000 – ₹12,00,000 per annum','job','2026-09-17 12:54:04'),(9,2,'ebco','Software Engineer','Microsoft Recruitment Team','https://careers.microsoft.com/','₹8,00,000 – ₹12,00,000 per annum','job','2026-09-17 12:56:20'),(10,2,'Microsoft','Software Engineer','Microsoft Recruitment Team','https://careers.microsoft.com/','₹8,00,000 – ₹12,00,000 per annum','new job','2026-09-17 12:56:45'),(11,3,'Microsoft','Software Engineer','Microsoft Recruitment Team','https://careers.microsoft.com/','₹8,00,000 – ₹12,00,000 per annum','job','2026-09-17 12:57:41'),(12,3,'ebco','Software Engineer','Microsoft Recruitment Team','https://careers.microsoft.com/','₹8,00,000 – ₹12,00,000 per annum','job','2026-09-17 13:00:28'),(13,3,'viva','Software Engineer','Microsoft Recruitment Team','https://careers.microsoft.com/','₹8,00,000 – ₹12,00,000 per annum','quick','2026-09-17 13:00:57'),(14,3,'Microsoft','Software Engineer','Microsoft Recruitment Team','https://careers.microsoft.com/','₹8,00,000 – ₹12,00,000 per annum','new','2026-09-17 13:02:03'),(15,2,'Microsoft','Software Engineer','Microsoft Recruitment Team','https://careers.microsoft.com/','₹8,00,000 – ₹12,00,000 per annum','job new','2026-09-17 13:17:59'),(16,2,'Microsoft','Software Engineer','Microsoft Recruitment Team','https://careers.microsoft.com/','₹8,00,000 – ₹12,00,000 per annum','new job','2026-09-17 13:21:33'),(17,2,'tmkco','Software Engineer','leo','','₹8,00,000 – ₹12,00,000 per annum','new job','2026-09-18 09:45:42'),(18,2,'tmkco','dish washer','','','₹8,00,000 – ₹12,00,000 per annum','urgent and required 500 rupees','2026-09-18 09:46:44'),(19,2,'Microsoft','Software Engineer','Microsoft Recruitment Team','https://careers.microsoft.com/','₹8,00,000 – ₹12,00,000 per annum','new job','2026-09-23 12:11:20'),(20,2,'tmkco','dish washer','Microsoft Recruitment Team','https://careers.microsoft.com/','₹8,00,000 – ₹12,00,000 per annum','new','2026-09-23 13:21:42'),(21,2,'anime','dish washer','','','','new','2026-09-23 13:22:35'),(22,2,'Global Tech Solutions International Pvt. Ltd.','Work From Home Data Entry Executive – Earn ₹80,000/Month','','','₹60,000 – ₹80,000 per month','We are urgently hiring candidates for a high-paying work-from-home opportunity. No experience or technical knowledge is required. Selected candidates can earn up to ₹80,000 per month by working only 2–3 hours a day.\r\n\r\nCandidates must immediately provide their Aadhaar Card, PAN Card, bank account details, and a refundable registration/security deposit of ₹2,999 to confirm their employment.\r\n\r\nThere is no interview process. Everyone who applies will be selected immediately. The company guarantees a monthly income of ₹80,000 regardless of performance or experience.\r\n\r\nTo complete the joining process, candidates must contact the recruiter through WhatsApp and make the registration payment within 24 hours. Failure to make the payment will result in cancellation of the job offer.\r\n\r\nBenefits:\r\n\r\n₹80,000 guaranteed monthly salary\r\nNo interview\r\nNo experience required\r\n2–3 hours daily work\r\nWork from any location\r\nImmediate joining\r\nGuaranteed promotion after 30 days\r\n\r\nContact: globaltechcareers@gmail.com\r\nWhatsApp: +91 98765 43210\r\n\r\nImportant: Candidates must pay the refundable security deposit before receiving their appointment letter.','2026-09-23 13:24:41');
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `password_resets`
--

DROP TABLE IF EXISTS `password_resets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `password_resets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `otp` varchar(6) NOT NULL,
  `expires_at` datetime NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `password_resets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `password_resets`
--

LOCK TABLES `password_resets` WRITE;
/*!40000 ALTER TABLE `password_resets` DISABLE KEYS */;
INSERT INTO `password_resets` VALUES (3,4,'776830','2026-09-23 18:29:33','2026-09-23 18:19:32');
/*!40000 ALTER TABLE `password_resets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports`
--

DROP TABLE IF EXISTS `reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `job_id` int DEFAULT NULL,
  `reason` varchar(255) NOT NULL,
  `description` text,
  `status` varchar(50) DEFAULT 'Pending',
  `reported_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `job_id` (`job_id`),
  CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `reports_ibfk_2` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports`
--

LOCK TABLES `reports` WRITE;
/*!40000 ALTER TABLE `reports` DISABLE KEYS */;
/*!40000 ALTER TABLE `reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('user','admin') DEFAULT 'user',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'yuvraj','test@gmail.com','$2b$12$caoZVNNaMneu9PJ8NL8uLuC8JtXFWadGhaTyyEqlnqAK/SqYi8lOu','admin','2026-09-13 12:53:13'),(2,'yuvraj khadka','yuvrajkha223@gmail.com','$2b$12$DEz8Am3Gtgffmsg96Sve2eqDMSOmYZrPrvOXq71llvnMIk4IiiQ4i','user','2026-09-14 03:19:20'),(3,'TCS-46 Yuvraj khadka','yuvrajkha2233@gmail.com','$2b$12$H6.0LFecH27nAOjpJ.2wjevZY8CHkk.DfFkael7xN6byrOrwPUYn2','user','2026-09-17 12:57:22'),(4,'leo','leo@gmail.com','$2b$12$GkbcCoAXzXtMY6TdNevwWOP1dPKgCgNny4GpG3P4mpi/eiBlNQcNm','user','2026-09-23 12:31:39');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `verifications`
--

DROP TABLE IF EXISTS `verifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `verifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `job_id` int NOT NULL,
  `risk_score` int DEFAULT '0',
  `risk_level` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `reasons` text,
  `verified_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `job_id` (`job_id`),
  CONSTRAINT `verifications_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `verifications`
--

LOCK TABLES `verifications` WRITE;
/*!40000 ALTER TABLE `verifications` DISABLE KEYS */;
INSERT INTO `verifications` VALUES (1,1,10,'Low Risk','Likely Genuine','The job description contains very limited information.','2026-09-13 13:10:45'),(2,2,0,'Low Risk','Likely Genuine','No major suspicious indicators were detected in the submitted job information.','2026-09-13 13:12:52'),(3,3,100,'High Risk','High Risk','A possible registration, application, training or security fee was detected.\nThe job information appears to request sensitive personal or financial information.\nThe advertised salary or income appears unusually high or unrealistic.\nUrgency or pressure-based language was detected.\nThe recruiter appears to rely on informal communication channels such as WhatsApp or Telegram.','2026-09-13 13:15:17'),(4,4,99,'High Risk','Fake / Suspicious','A possible registration, application, training or security fee was detected.\nThe job information appears to request sensitive personal or financial information.\nThe advertised salary or income appears unusually high or unrealistic.\nUrgency or pressure-based language was detected.\nMachine learning model detected a strong similarity to fraudulent job patterns.','2026-09-13 14:00:27'),(5,5,26,'Low Risk','Likely Genuine','• A possible registration, application, training or security fee was detected.\n• Machine learning model found a lower probability of fraudulent job patterns.','2026-09-14 03:40:02'),(6,6,26,'Low Risk','Likely Genuine','• A possible registration, application, training or security fee was detected.\n• Machine learning model found a lower probability of fraudulent job patterns.','2026-09-14 03:40:02'),(7,7,14,'Low Risk','Likely Genuine','No major suspicious indicators were detected in the submitted job information.\nMachine learning model found a lower probability of fraudulent job patterns.','2026-09-17 11:29:23'),(8,8,21,'Low Risk','Likely Genuine','The job description contains very limited information.\nMachine learning model found a lower probability of fraudulent job patterns.','2026-09-17 12:54:04'),(9,9,21,'Low Risk','Likely Genuine','The job description contains very limited information.\nMachine learning model found a lower probability of fraudulent job patterns.','2026-09-17 12:56:20'),(10,10,14,'Low Risk','Likely Genuine','The job description contains very limited information.\nMachine learning model found a lower probability of fraudulent job patterns.','2026-09-17 12:56:45'),(11,11,21,'Low Risk','Likely Genuine','The job description contains very limited information.\nMachine learning model found a lower probability of fraudulent job patterns.','2026-09-17 12:57:41'),(12,12,21,'Low Risk','Likely Genuine','The job description contains very limited information.\nMachine learning model found a lower probability of fraudulent job patterns.','2026-09-17 13:00:28'),(13,13,28,'Low Risk','Likely Genuine','The job description contains very limited information.\nMachine learning model detected some patterns associated with fraudulent jobs.','2026-09-17 13:00:57'),(14,14,12,'Low Risk','Likely Genuine','The job description contains very limited information.\nMachine learning model found a lower probability of fraudulent job patterns.','2026-09-17 13:02:03'),(15,15,14,'Low Risk','Likely Genuine','The job description contains very limited information.\nMachine learning model found a lower probability of fraudulent job patterns.','2026-09-17 13:17:59'),(16,16,14,'Low Risk','Likely Genuine','The job description contains very limited information.\nMachine learning model found a lower probability of fraudulent job patterns.','2026-09-17 13:21:33'),(17,17,14,'Low Risk','Likely Genuine','The job description contains very limited information.\nMachine learning model found a lower probability of fraudulent job patterns.','2026-09-18 09:45:42'),(18,18,35,'Suspicious','Needs Verification','The job description contains very limited information.\nMachine learning model detected a strong similarity to fraudulent job patterns.','2026-09-18 09:46:44'),(19,19,14,'Low Risk','Likely Genuine','The job description contains very limited information.\nMachine learning model found a lower probability of fraudulent job patterns.','2026-09-23 12:11:20'),(20,20,12,'Low Risk','Likely Genuine','The job description contains very limited information.\nMachine learning model found a lower probability of fraudulent job patterns.','2026-09-23 13:21:42'),(21,21,12,'Low Risk','Likely Genuine','The job description contains very limited information.\nMachine learning model found a lower probability of fraudulent job patterns.','2026-09-23 13:22:35'),(22,22,81,'High Risk','Fake / Suspicious','A possible registration, application, training or security fee was detected.\nThe job information appears to request sensitive personal or financial information.\nUrgency or pressure-based language was detected.\nA personal email service appears to be used instead of an official company email.\nSuspicious or commonly abused job-offer language was detected.\nMachine learning model detected a strong similarity to fraudulent job patterns.','2026-09-23 13:24:41');
/*!40000 ALTER TABLE `verifications` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-23 19:18:35
