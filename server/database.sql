DROP DATABASE idp_project;
CREATE DATABASE idp_project;
USE idp_project;

CREATE TABLE `Lamp` (
  `LampID` INT,
  `Klas` VARCHAR(20),
  PRIMARY KEY (`LampID`)
);

CREATE TABLE `Sessie` (
  `SessieID` INT AUTO_INCREMENT,
  `Gemiddelde` FLOAT,
  `Starttijd` DATETIME,
  `Eindtijd` DATETIME,
  `DocentID` INT,
  `LampID` INT,
  PRIMARY KEY (`SessieID`)
);

CREATE TABLE `Docent` (
  `DocentID` INT AUTO_INCREMENT,
  `Gebruikersnaam` VARCHAR(50),
  `Wachtwoord` VARCHAR(65),
  `Email` VARCHAR(50),
  PRIMARY KEY (`DocentID`)
);

ALTER TABLE Sessie
ADD CONSTRAINT Sessie_Docent
FOREIGN KEY (DocentID)
	REFERENCES Docent(DocentID)
	ON UPDATE CASCADE
    ON DELETE CASCADE;
ALTER TABLE Sessie
ADD CONSTRAINT Sessie_Lamp
FOREIGN KEY (LampID)
	REFERENCES Lamp(LampID)
	ON UPDATE CASCADE
	ON DELETE CASCADE;

#Jan123
INSERT INTO Docent (Gebruikersnaam, Wachtwoord, Email)
VALUES ('Jan_Bakker', 'e1e1bd40ea9a6d9ee5471cfbb6c05f1c17cde51c08051984b7614682cc3af91b', 'jan.bakker@mail.com');

#Piet123
INSERT INTO Docent (Gebruikersnaam, Wachtwoord, Email)
VALUES ('Piet_Wit', '178277322005c96787e9a5f41663fa5954cd2bc9d9f7e83a51a7e285fc7b112a', 'piet.wit@mail.com');

#Boris123
INSERT INTO Docent (Gebruikersnaam, Wachtwoord, Email)
VALUES ('Boris_Wilde', 'dd70d6f8a832a3a5f864bf7db06f0d9227bbc40a6b94b92ec5a183703a737c60', 'boris.wilde@mail.com');

#Eva123
INSERT INTO Docent (Gebruikersnaam, Wachtwoord, Email)
VALUES ('Eva_Dijk', '0f78bd7e70df81b87f6e7d97ec2d30779a96720448219f97977a81def3552c4d', 'eva.dijk@mail.com');

#Sara123
INSERT INTO Docent (Gebruikersnaam, Wachtwoord, Email)
VALUES ('Sara_Bruin', 'fb9a8e82593874c818f11adffdb0e86869800c39cc3da5676e16c39d77a32ec4', 'sara.bruin@mail.com');

INSERT INTO Lamp (LampID, Klas)
VALUES (1, 'A6');
