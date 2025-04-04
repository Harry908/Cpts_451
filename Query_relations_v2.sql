CREATE TABLE business (
    business_id VARCHAR(30) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    stars NUMERIC(2,1) CHECK (stars >= 0 AND stars <= 5),
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zipcode VARCHAR(20),
    numCheckins INT DEFAULT 0 CHECK (numCheckins >= 0),
    is_open BOOLEAN NOT NULL,
    reviewrating NUMERIC(2,1) DEFAULT 0.0 CHECK (reviewrating >= 0 AND reviewrating <= 5),
    reviewcount INT DEFAULT 0 CHECK (reviewcount >= 0)
);

CREATE TABLE business_category (
    business_id VARCHAR(30) NOT NULL,
    cname VARCHAR(100) NOT NULL,
    PRIMARY KEY (business_id, cname),
    FOREIGN KEY (business_id) REFERENCES business(business_id) ON DELETE CASCADE
);

CREATE TABLE business_attribute (
    business_id VARCHAR(30) NOT NULL,
    aname VARCHAR(100) NOT NULL,
    value TEXT NOT NULL,
    PRIMARY KEY (business_id, aname),
    FOREIGN KEY (business_id) REFERENCES business(business_id) ON DELETE CASCADE
);

CREATE TABLE business_check_in (
    business_id VARCHAR(30) NOT NULL,
    day VARCHAR(10) NOT NULL,
    hour TIME NOT NULL,
    count INT DEFAULT 0 CHECK (count >= 0),
    PRIMARY KEY (business_id, day, hour),
    FOREIGN KEY (business_id) REFERENCES business(business_id) ON DELETE CASCADE
);

CREATE TABLE yelp_user (
    user_id VARCHAR(30) PRIMARY KEY,
    name VARCHAR(100),
    review_count INT DEFAULT 0,
    yelping_since DATE,
    useful INT DEFAULT 0,
    funny INT DEFAULT 0,
    cool INT DEFAULT 0,
    fans INT DEFAULT 0,
    average_stars NUMERIC(3,2) CHECK (average_stars >= 0 AND average_stars <= 5)
);

CREATE TABLE review (
    review_id VARCHAR(30) PRIMARY KEY,
    business_id VARCHAR(30) NOT NULL,
    user_id VARCHAR(30) NOT NULL,
    stars SMALLINT CHECK (stars >= 0 AND stars <= 5),
    date DATE NOT NULL,
    text TEXT,
    FOREIGN KEY (business_id) REFERENCES business(business_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES yelp_user(user_id) ON DELETE CASCADE
);
