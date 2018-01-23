CREATE TABLE Docent  (
DocentID INT,
Gebruikersnaam VARCHAR(50),
Wachtwoord VARCHAR(50),
Email VARCHAR(50),
PRIMARY KEY(DocentID)
);

CREATE TABLE Klas  (
KlasID INT,
DocentID INT,
LampID INT,
PRIMARY KEY(KlasID)
);

CREATE TABLE Lamp  (
LampID INT,
SensorID INT,
PRIMARY KEY(LampID)
);

CREATE TABLE Sensor  (
SensorID INT,
Decibel INT,
PRIMARY KEY(SensorID)
);


ALTER TABLE lamp
ADD CONSTRAINT fk_lamp
FOREIGN KEY (SensorID) REFERENCES sensor(SensorID) ;

CREATE INDEX idx_DocentID ON klas (DocentID) ;

ALTER TABLE docent
ADD CONSTRAINT fk_Docent
FOREIGN KEY (DocentID) REFERENCES klas(DocentID);

CREATE INDEX idx_LampID ON klas (LampID) ;

ALTER TABLE lamp
ADD CONSTRAINT fk_lamp
FOREIGN KEY (LampID) REFERENCES klas(LampID);