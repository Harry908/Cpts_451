CREATE TABLE business (
    business_id VARCHAR(30) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    stars NUMERIC(2,1) CHECK (stars >= 0 AND stars <= 5),
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zipcode VARCHAR(20),
    total_check_in INT DEFAULT 0 CHECK (total_check_in >= 0),
    is_open BOOLEAN NOT NULL,
    avg_rating_stars NUMERIC(2,1) CHECK (avg_rating_stars >= 0 AND avg_rating_stars <= 5),
    review_count INT DEFAULT 0 CHECK (review_count >= 0)
);

CREATE TABLE business_category (
    business_id VARCHAR(30) NOT NULL,
    cname VARCHAR(100) NOT NULL,
    PRIMARY KEY (business_id, cname),
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE business_attribute (
    business_id VARCHAR(30) NOT NULL,
    aname VARCHAR(100) NOT NULL,
    value BOOLEAN NOT NULL,
    PRIMARY KEY (business_id, aname),
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE business_check_in (
    business_id VARCHAR(30) NOT NULL,
    day VARCHAR(10) NOT NULL,
    hour TIME NOT NULL,
    count INT DEFAULT 0 CHECK (count >= 0),
    PRIMARY KEY (business_id, day, hour),
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE review (
    review_id VARCHAR(30) PRIMARY KEY,
    business_id VARCHAR(30) NOT NULL,
    stars SMALLINT CHECK (stars >= 0 AND stars <= 5),
    date DATE NOT NULL,
    text TEXT,
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);