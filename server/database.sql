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
  `Wachtwoord` VARCHAR(50),
  `Email` VARCHAR(50),
  PRIMARY KEY (`DocentID`)
);

ALTER TABLE Sessie
ADD CONSTRAINT Sessie_Docent
FOREIGN KEY (DocentID) REFERENCES Docent(DocentID),
ADD CONSTRAINT Sessie_Lamp
FOREIGN KEY (LampID) REFERENCES Lamp(LampID);


INSERT INTO Docent (Gebruikersnaam, Wachtwoord, Email)
VALUES ('Jan_Bakker', 'Jan123', 'jan.bakker@mail.com');

INSERT INTO Docent (Gebruikersnaam, Wachtwoord, Email)
VALUES ('Piet_Wit', 'Piet123', 'piet.wit@mail.com');

INSERT INTO Docent (Gebruikersnaam, Wachtwoord, Email)
VALUES ('Boris_Wilde', 'Boris123', 'boris.wilde@mail.com');

INSERT INTO Docent (Gebruikersnaam, Wachtwoord, Email)
VALUES ('Eva_Dijk', 'Eva123', 'eva.dijk@mail.com');

INSERT INTO Docent (Gebruikersnaam, Wachtwoord, Email)
VALUES ('Sara_Bruin', 'Sara123', 'sara.bruin@mail.com');

INSERT INTO Lamp (LampID, Klas)
VALUES (1, 'A6');
