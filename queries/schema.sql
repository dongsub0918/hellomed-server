CREATE TABLE ebdb.check_ins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthDate DATE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(255) NOT NULL,
    hearAboutUs VARCHAR(255),
    address TEXT,
    medicationAllergy TEXT,
    preferredPharmacy VARCHAR(255),
    homeMedication TEXT,
    reasonForVisit TEXT,
    exposures TEXT,
    recentTests TEXT,
    recentVisits TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
