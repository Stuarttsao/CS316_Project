-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    uid INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL
    -- address VARCHAR(255) NOT NULL
);

-- CREATE TABLE Products (
--     id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
--     name VARCHAR(255) UNIQUE NOT NULL,
--     price DECIMAL(12,2) NOT NULL,
--     available BOOLEAN DEFAULT TRUE
-- );

-- CREATE TABLE Purchases (
--     id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
--     uid INT NOT NULL REFERENCES Users(id),
--     pid INT NOT NULL REFERENCES Products(id),
--     time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
-- );

CREATE TABLE Menus (
    uid INT NOT NULL REFERENCES Users(uid),
    name VARCHAR(255) NOT NULL,
    time_made timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    summary VARCHAR(8000) NOT NULL,
    PRIMARY KEY(uid, name)

);

CREATE TABLE MenuDrinks(
    FOREIGN KEY(uid, menuName) REFERENCES Menus(uid, name),
    FOREIGN KEY(did) REFERENCES Drinks(did),
    PRIMARY KEY(uid, menuName, did)
);

CREATE TABLE Drinks(
    did INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    category VARCHAR(255) NOT NULL,
    picture VARCHAR(8000),
    instructions VARCHAR(8000) NOT NULL
    -- description VARCHAR(8000) NOT NULL
);

CREATE TABLE Ingredients(
    iid INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(8000) NOT NULL
);

CREATE TABLE Components(
    iid INT NOT NULL REFERENCES Ingredients(iid),
    did INT NOT NULL REFERENCES Drinks(did),
    amount FLOAT NOT NULL,
    unit VARCHAR(255) NOT NULL,
    PRIMARY KEY(iid, did),
    FOREIGN KEY(iid) REFERENCES Ingredients(iid),
    FOREIGN KEY(did) REFERENCES Drinks(did)
);

CREATE TABLE Ratings(
    uid Int NOT NULL REFERENCES Users(uid),
    did Int NOT NULL REFERENCES Drinks(did),
    time_rated timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    score INT NOT NULL,
    CONSTRAINT score_ck CHECK (score BETWEEN 0 AND 5),
    descript VARCHAR(8000),
    likes INT NOT NULL,
    dislikes INT NOT NULL,
    --PRIMARY KEY(uid,did), GO BACK AND ENFORCE UNIQUENESS
    FOREIGN KEY(uid) REFERENCES Users(uid),
    FOREIGN KEY(did) REFERENCES Drinks(did)
);

-- CREATE TABLE ingredientCart(
--     FOREIGN KEY(uid) REFERENCES Users(uid),
--     FOREIGN KEY(iid) REFERENCES Ingredients(iid),
--     amount FLOAT NOT NULL,
--     unit VARCHAR(255) NOT NULL,
--     PRIMARY KEY(uid,iid)
-- );

-- CREATE TABLE barCart(
--     FOREIGN KEY(uid) REFERENCES Users(uid),
--     FOREIGN KEY(iid) REFERENCES Ingredients(did),
--     times_made INT NOT NULL
-- ):