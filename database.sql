CREATE DATABASE idp_project
CREATE TABLE Docent  (
DocentID INT NOT NULL AUTO_INCREMENT,
Gebruikersnaam VARCHAR(50),
Wachtwoord VARCHAR(50),
Email VARCHAR(50),
PRIMARY KEY(DocentID)
);
CREATE TABLE Klas  (
KlasID INT NOT NULL AUTO_INCREMENT,
DocentID INT NOT NULL,
LampID INT NOT NULL,
PRIMARY KEY(KlasID)
);

CREATE TABLE Lamp  (
LampID INT NOT NULL AUTO_INCREMENT,
SensorID INT NOT NULL ,
PRIMARY KEY(LampID)
);

CREATE TABLE Sensor  (
SensorID INT NOT NULL AUTO_INCREMENT,
Decibel INT NOT NULL,
PRIMARY KEY(SensorID)
);


ALTER TABLE Klas
ADD CONSTRAINT Klas_Docent
FOREIGN KEY (DocentID) REFERENCES Docent(DocentID);

ALTER TABLE Klas
ADD CONSTRAINT Klas_Lamp
FOREIGN KEY (LampID) REFERENCES Lamp(LampID);

ALTER TABLE Lamp
ADD CONSTRAINT Lamp_Sensor
FOREIGN KEY (SensorID) REFERENCES Sensor(SensorID);
INSERT INTO docent (Gebruikersnaam, Wachtwoord, Email)
VALUES ('Jan_Bakker', 'Jan123', 'jan.bakker@mail.com')

INSERT INTO docent (Gebruikersnaam, Wachtwoord, Email)
VALUES ('Piet_Wit', 'Piet123', 'piet.wit@mail.com')

INSERT INTO docent (Gebruikersnaam, Wachtwoord, Email)
VALUES ('Boris_Wilde', 'Boris123', 'boris.wilde@mail.com')

INSERT INTO docent (Gebruikersnaam, Wachtwoord, Email)
VALUES ('Eva_Dijk', 'Eva123', 'eva.dijk@mail.com')

INSERT INTO docent (Gebruikersnaam, Wachtwoord, Email)
VALUES ('Sara_Bruin', 'Sara123', 'sara.bruin@mail.com')
