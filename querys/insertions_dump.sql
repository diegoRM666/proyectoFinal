INSERT INTO `cliente` VALUES 
(1,'Telcel','5539005436','telcel@test.com','Lago Alberto 60, Col. Polanco, CP. 54090','Telcel Polanco'),
(2,'Inbursa','5530104575','inbursa@test.com.mx','Nextengo 78, Col. Santa Cruz Acayucan, C.P. 02770',''),
(3,'Coppel','800-220-7735','coppel@test.com','Av. Ermita Iztapalapa #3417, 09640, Ciudad de México',''),
(4,'Bancomer','52262663','bancome@test.com','Av. Paseo de la Reforma s/n','Torre Bancomer'),
(5,'Multiva','5555156066','multiva@test.com','Agrarismo 208, Miguel Hidalgo','Cajero ATM');

INSERT INTO `miembro` VALUES (1,'Diego Ruiz','5530104575','diego.ruiz@apptec.com.mx','Juan De La Barrera 6','No Disponible','En Actividad',''),
(2,'Victor Reyes','5545056725','victor.reyes@apptec.com.mx','Calzada Legaria 85','Disponible','Libre','Miembro Foraneo'),
(3,'Santiago Tovar','5539005436','santiago.tovar@apptec.com.mx','Avenida de Las Palmas s/n','Disponible','Libre','Miembro Foraneo');

INSERT INTO `recurso` VALUES (1,'Llave Allen','Herramienta','Llave Allen 3/4','Mecánica','ALL1513','En Uso','10 Años',''),
(2,'Kit de Desarmadores','Herramienta','12 Desarmadores','Mecánica','KD121223','En Stock','10 Años',''),
(3,'Kit de Dados','Herramienta','Kit de 12 Dados','Mecánica','DA90313','En Stock','10 Años',''),
(4,'Inyector de Tinta','Material','Inyector de Tinta Pitney Bowes','Insumo','PBI12312104','En Stock','1 Vez','Para el Modelo 556892A'),
(5,'Kit de Herramientas','Herramienta','Juego de 6 Desarmadores','Mecánica','KHs5272','En Stock','10 Años','');

INSERT INTO `actividad` VALUES (2,'Reemplazo Inyector Tinta','2024-12-12',NULL,'unknown',NULL,'Matenimiento','Abierto',1,1);
