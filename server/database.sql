DROP DATABASE idp_project;
CREATE DATABASE idp_project;
USE idp_project;

CREATE TABLE Docent  (
DocentID INT NOT NULL AUTO_INCREMENT,
Gebruikersnaam VARCHAR(50),
Wachtwoord VARCHAR(50),
Email VARCHAR(50),
PRIMARY KEY(DocentID)
);


CREATE TABLE Lamp  (
LampID INT NOT NULL AUTO_INCREMENT,
SensorID INT NOT NULL ,
PRIMARY KEY(LampID)
);

CREATE TABLE Sensor  (
SensorID INT NOT NULL AUTO_INCREMENT,
LampID INT NOT NULL ,
Tijd DATETIME,
PRIMARY KEY(SensorID)
);

ALTER TABLE Lamp
ADD CONSTRAINT Lamp_Sensor
FOREIGN KEY (SensorID) REFERENCES Sensor(SensorID);

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

INSERT INTO Sensor (SensorID, LampID)
VALUES ('1', '001');

INSERT INTO Sensor (SensorID, LampID)
VALUES ('2', '001');

INSERT INTO Sensor (SensorID, LampID)
VALUES ('3', '001');

INSERT INTO lamp (LampID, SensorID)
VALUES ('001', '1'); #2 en 3 moeten er ook nog bij#

#decibel en Gem_Decibel en DocentID bij lamp en foreign key van docent_lamp moeten er nog bij#