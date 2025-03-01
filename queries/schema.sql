CREATE TABLE ebdb.check_ins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthDate DATE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(255) NOT NULL,
    hearAboutUs VARCHAR(255),
    address TEXT NOT NULL,
    zipcode VARCHAR(16) NOT NULL,
    preferredPharmacy VARCHAR(255) NOT NULL,
    medicationAllergy TEXT,
    homeMedication TEXT,
    reasonForVisit TEXT NOT NULL,
    exposures TEXT,
    recentTests TEXT,
    recentVisits TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ebdb.admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    CHECK (email REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
);