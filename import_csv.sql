CREATE TABLE restaurants (
    Name TEXT,
    Address TEXT,
    Location TEXT,
    Price TEXT,
    Cuisine TEXT,
    Longitude REAL,
    Latitude REAL,
    PhoneNumber TEXT,
    Url TEXT,
    WebsiteUrl TEXT,
    Award TEXT,
    GreenStar INTEGER,
    FacilitiesAndServices TEXT,
    Description TEXT,
    PRIMARY KEY (Name, Address)
);

.import --csv --skip 1 michelin_my_maps.csv restaurants
