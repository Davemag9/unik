CREATE TABLE ServiceCenter(
	ServiceCenterID int ,
	dayOffID int NOT NULL,
	city varchar(64) NOT NULL,
	income int NOT NULL,
	PRIMARY KEY (ServiceCenterID)
);

CREATE TABLE Master(
	masterID int NOT NULL,
	lastName varchar(64) NOT NULL,
	qualification int NOT NULL,
	ServiceCenterID int NOT NULL,
	PRIMARY KEY (masterID),
	
	CONSTRAINT fk_SCID 
		FOREIGN KEY (ServiceCenterID) 
			REFERENCES ServiceCenter(ServiceCenterID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE devOwner(
	ownerID int NOT NULL,
	lastName varchar(64) NOT NULL,
	phone varchar(10),
	PRIMARY KEY (ownerID)
);

CREATE TABLE DeviceType(
	typeID int NOT NULL,
	typeName varchar(16) NOT NULL,
	description text,
	PRIMARY KEY (typeID)
);

CREATE TABLE Device(
	deviceID int NOT NULL,
	color varchar(16),
	batteryCapacity int,
	devicePerformance int,
	ownerID int NOT NULL,
	typeID int NOT NULL,
	PRIMARY KEY (deviceID),
	
	CONSTRAINT fk_ownrID
		FOREIGN KEY (ownerID) 	
			REFERENCES devOwner(ownerID) ON DELETE CASCADE ON UPDATE CASCADE,
	
	CONSTRAINT fk_tpID
		FOREIGN KEY (typeID) 
			REFERENCES DeviceType(typeID) ON DELETE NO ACTION ON UPDATE CASCADE
	
);

CREATE TABLE DeviceInfo(
	serialNumber int NOT NULL,
	price int NOT NULL,
	age int,
	deviceID int NOT NULL,
	PRIMARY KEY (serialNumber),
	
	CONSTRAINT fk_devID
		FOREIGN KEY (deviceID) 
			REFERENCES Device(deviceID)
);
	
CREATE TABLE Offer(
	offerID int NOT NULL,
	receiptData date NOT NULL,
	deviceState varchar(128),
	masterID int NOT NULL,
	deviceID int NOT NULL, 
	PRIMARY KEY (offerID),
	
	CONSTRAINT fk_mstrID
		FOREIGN KEY (masterID) 
			REFERENCES Master(masterID) ON DELETE CASCADE ON UPDATE CASCADE,
	
	CONSTRAINT fk_devID
		FOREIGN KEY (deviceID) 
			REFERENCES Device(deviceID) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE Problem(
	problemID int NOT NULL,
	priceToSolve int NOT NULL,
	description text,
	PRIMARY KEY (problemID)
);

CREATE TABLE ProblemOffer(
	offerID int NOT NULL,
	problemID int NOT NULL,
	CONSTRAINT fk_offrID 
		FOREIGN KEY (offerID) 
			REFERENCES Offer(offerID) ON DELETE CASCADE ON UPDATE NO ACTION,
	CONSTRAINT fk_prblID 
		FOREIGN KEY (problemID) 
			REFERENCES Problem(problemID) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE Details(
	detailsID int NOT NULL,
	detailName varchar(32) NOT NULL,
	detailPrice int NOT NULL,
	supplier int NOT NULL,
	problemID int NOT NULL, 
	PRIMARY KEY (detailsID),
	CONSTRAINT fk_prblID 
		FOREIGN KEY (problemID) 
			REFERENCES Problem(problemID) ON DELETE CASCADE ON UPDATE NO ACTION
);
