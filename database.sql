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
